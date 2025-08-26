# 📚 Research Papers Review Assistant  

An **AI-powered literature review assistant** built with **Streamlit** and **Microsoft AutoGen (multi-agent framework)**.  
The app helps researchers explore a topic by automatically finding and summarizing research papers through a structured **two-agent conversation**.  

---

## 🚀 Features  
1. 🔍 **Topic-based Research** – Enter a research topic and specify how many papers you want to review.  
2. 🤖 **Multi-Agent Workflow with AutoGen** – Uses Microsoft AutoGen to create collaborating agents (Retriever + Reviewer) for research surveys.  
3. ⏳ **Real-Time Streaming** – Watch the agent conversation stream live in the Streamlit UI.  
4. 🎨 **Custom UI** – Clean interface with watermark branding for personalization.  
5. ⚡ **Async Execution** – Built with `asyncio` for responsive streaming even with longer queries.  

---

## 🛠️ Tech Stack  
- **Python**  
- **Streamlit** (Frontend UI)  
- **Microsoft AutoGen** (Agent framework for collaboration)   
- **Asyncio** (Efficient streaming)  

---

## 📂 Project Structure  

├── agents_with_logic.py # Defines AutoGen-based multi-agent survey logic

├── streamlit_app.py # Streamlit frontend with watermark UI

├── requirements.txt # Dependencies


## ▶️ Run Locally  

   git clone https://github.com/suniljohn-ai/Autogen_microsoft.git

   
Install dependencies:

pip install -r requirements.txt

Run the app:
streamlit run streamlit_app.py

📌 Example Usage
Input: Agentic AI

Output: AutoGen agents collaborate and stream summarized findings from recent papers.

⚠️ Note
You must add a valid OpenAI API key (or alternative LLM provider key) in agents_with_logic.py.

