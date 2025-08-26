'''
agents_with_logic.py
====================
it is the core logic for multi-agent literature and review agents built with the
** AutoGen ** AgentChat AI stack.
it exposes a single coroutine 'run_agents()' that drives a two-agent team

 ** researcher_agent ** - built for crafting an arXiv query and prepares the related
 researched papers via the provided arXiv search tool
 ** summarizer_agent ** - built for summarizing the provided researched papers by *researcher_agent*
 and provides summary with some parameters like name, description and so on

this module is more self-contained so we can use it in CLI apps, Streamlit, FastAPI, Gradio
we are going to use Streamlit for us

'''

# step 1: importing the required libraries
# ========================================

from __future__ import annotations
import os
import asyncio
from typing import AsyncGenerator, List, Dict

import arxiv
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ( TextMessage )
from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_ext.models.openai import OpenAIChatCompletionClient

api_key = os.getenv("OPENROUTER_API_KEY")

# 1. defining tools for the models
# ================================
def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """Return a compact list of arXiv papers matching *query*.

        Each element contains: ``title``, ``authors``, ``published``, ``summary`` and
        ``pdf_url``.  The helper is wrapped as an AutoGen *FunctionTool*, below so it
        can be invoked by agents through the normal tool‑use mechanism.
        """
    client = arxiv.Client()
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance,
    )
    papers: List[Dict] = []

    for result in client.results(search):
        papers.append(
            {
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "published": result.published.strftime("%y-%m-%d"),
                "summary": result.summary,
                "pdf_url": result.pdf_url,
            }

        )
    return papers

arxiv_tool = FunctionTool(
    arxiv_search,
    description = (
        "Searches arXiv and returns up to *max_results* papers, each containing "
        "title, authors, publication date, abstract, and pdf_url."
    ),
)

# 2. Defining Agent and team factory
# ==================================
def built_team(model: str= "deepseek/deepseek-r1-0528:free") -> RoundRobinGroupChat:
    """ Create and Return a two agent *RoundRobinGroupChat* team """
    llm_client = OpenAIChatCompletionClient(
        base_url = "https://openrouter.ai/api/v1",
        model = model,
        api_key = os.getenv("OPENROUTER_API_KEY"),
        model_info = {
            "family": "deepseek",
            "vision": True,
            "function_calling": True,
            "json_output": False,
        }
    )
    # agent that can **only** calls the arxiv tool and forwards only top-N papers
    search_agent = AssistantAgent(
        name = "Search_agent",
        description = "Crafts arXiv queries and retrieves candidate papers.",
        system_message = (
            "Given a user topic, think of the best arXiv query and call the "
            "provided tool. Always fetch five‑times the papers requested so "
            "that you can down‑select the most relevant ones. When the tool "
            "returns, choose exactly the number of papers requested and pass "
            "them as concise JSON to the summarizer."
        ),
        model_client = llm_client,
        tools = [arxiv_tool],
        reflect_on_tool_use = True,
    )

    summarizer_agent = AssistantAgent(
        name = "summarizer_agent",
        description = "Produces a short Markdown review from provided papers.",
        system_message = (
            "You are an expert researcher. When you receive the JSON list of "
            "papers, write a literature‑review style report in Markdown:\n" 
            "1. Start with a 2–3 sentence introduction of the topic.\n" 
            "2. Then include one bullet per paper with: title (as Markdown "
            "link), authors, the specific problem tackled, and its key "
            "contribution.\n" 
            "3. Close with a single‑sentence takeaway."
        ),
        model_client = llm_client,
    )

    return RoundRobinGroupChat(
        participants = [search_agent, summarizer_agent],
        max_turns = 20,
    )

# Step 3: defining the Orchestrations
# =====================================

async def run_survey(
        topic: str,
        num_papers: int = 5,
        model: str = "deepseek/deepseek-r1-0528:free",
) -> AsyncGenerator[str, None]:
    """ Yields strings representing conversations in real-time"""

    team = built_team(model=model)
    task_prompt = (
        f"conduct a literature review on **{topic}** and return exactly {num_papers} of papers"
    )

    async for msg in team.run_stream(task = task_prompt):
        if isinstance(msg, TextMessage):
            yield f"{msg.source}:{msg.content}"


# step 4: checking with CLI
# ==========================

if __name__ == "__main__":
    async def _demo() -> None:
        async for line in run_survey("Artificial Intelligence", num_papers = 5):
            print(line)
    asyncio.run(_demo())
