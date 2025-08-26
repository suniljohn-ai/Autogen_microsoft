'''
streamlit_app.py
================
A minimal Streamlit frontend for the literature‑review assistant defined in
`agents_with_logic.py`.  Users enter a topic and the desired number of papers, then
watch the two‑agent conversation stream in real‑time.
'''

import asyncio
import streamlit as st

from agents_with_logic import run_survey

#defifining page config and title for the frontend
st.set_page_config(page_title="Research Papers Review Assistant", page_icon="📚")
st.title("📚 Research Papers Review Assistant")

st.markdown(
    """
    <style>
    /* Bottom-right corner watermark with link */
    .watermark-corner {
        position: fixed;
        right: 12px;
        bottom: 8px;
        opacity: 0.7;
        font-size: 13px;
        font-family: Arial, sans-serif;
        color: #fff;
        z-index: 9999;
        pointer-events: auto; /* allow clicking */
        user-select: none;
    }
    .watermark-corner a {
        color: #fff; /* White text */
        text-decoration: none;
    }
    .watermark-corner a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="watermark-corner">
        <a href="https://www.linkedin.com/in/sunil-kumar-369-/" target="_blank">
            © Sunil Kumar Nallabothula
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

#query =
query = st.text_input("Enter your Research Topic")
#n_papers =
n_papers = st.slider("no_of_papers",1,10,5)

if st.button("Enter") and query:

    async def _runner() -> None:
        chat_placeholder = st.container()
        async for frame in run_survey(query, num_papers=n_papers):
            role, *rest = frame.split(":",1)
            content = rest[0].strip() if rest else ""
            with chat_placeholder:
                with st.chat_message("assistant"):
                    st.markdown(f"**{role}**, {content}")

    with st.spinner("Working6/MSP..."):
        try:
            asyncio.run(_runner())
        except RuntimeError:
            # fallbacks when an event is already running(e.g Streamlit cloud)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_runner())

    st.success("the Research Papers Review is completed please check the results 🎉h")

st.text("Note: Please Note if you are getting an OpenAIError, then it causing an llm error, because we've revoked the api key ")

