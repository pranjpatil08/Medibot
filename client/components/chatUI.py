import streamlit as st
from utils.api import ask_question
import re

def is_greeting(text: str) -> bool:
    t = text.strip().lower()
    return bool(re.fullmatch(
        r"(hi|hello|hey|hii+|heyy+|yo|good\s*morning|good\s*afternoon|good\s*evening)",
        t
    ))

MED_ACTIONS = {
    "Summarize this PDF": "Give a structured medical summary of this document with key takeaways and important notes.",
    "List key topics": "List the key medical topics covered in this document as bullet points.",
    "Symptoms mentioned": "From this document, list the symptoms mentioned and briefly explain each.",
    "Causes mentioned": "From this document, list possible causes mentioned and explain them briefly.",
    "Red flags / When to seek care": "From this document, list warning signs or when to seek medical care. If not mentioned, say 'Not specified in the document.'",
    "Define medical terms": "Extract important medical terms from this document and define them in simple language.",
}

def render_chat():
    st.markdown("""
    <style>
    /* Put some space so messages don't hide behind the sticky input */
    section.main {
    padding-bottom: 110px !important;
    }

    /* Make chat input sticky INSIDE the main layout (so it reflows with sidebar) */
    div[data-testid="stChatInput"]{
    position: sticky !important;
    bottom: 0 !important;

    /* key: no fixed centering, let Streamlit layout control width */
    left: auto !important;
    right: auto !important;
    transform: none !important;
    width: 100% !important;

    background: #0f1117;
    padding: 8px 10px;
    border-top: 1px solid #2a2f3a;
    border-radius: 12px 12px 0 0;
    z-index: 50;
    }

    /* Make textbox single-line and smaller */
    div[data-testid="stChatInput"] textarea{
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    line-height: 1.2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("💬 Chat with your medical PDFs")

    pdfs = st.session_state.get("uploaded_pdf_names", [])

    if pdfs:
        if "selected_pdf" not in st.session_state:
            st.session_state["selected_pdf"] = pdfs[0]

        st.session_state["selected_pdf"] = st.selectbox(
            "Select medical PDF",
            pdfs,
            index=pdfs.index(st.session_state.get("selected_pdf", pdfs[0]))
        )
    else:
        st.info("Upload a medical PDF to start.")
        return

    
    with st.expander("🧰 Medical Actions (one-click)", expanded=True):
        cols = st.columns(3)
        action_keys = list(MED_ACTIONS.keys())

        clicked_action = None
        for i, label in enumerate(action_keys):
            if cols[i % 3].button(label, use_container_width=True):
                clicked_action = label

        if clicked_action:
            action_prompt = MED_ACTIONS[clicked_action]
            st.session_state.setdefault("messages", [])
            st.session_state.messages.append({"role": "user", "content": action_prompt})

            
            st.chat_message("user").markdown(action_prompt)

            resp = ask_question(action_prompt, selected_pdf=st.session_state["selected_pdf"])
            if resp.status_code == 200:
                data = resp.json()
                answer = data.get("response", "")
                sources = data.get("sources", [])

                st.chat_message("assistant").markdown(answer)

                if sources:
                    st.markdown("📄 **Sources:**")
                    for src in sources:
                        st.markdown(f"- `{src}`")

                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.markdown(
                    """
                    <div style="
                        background-color:#1f2933;
                        color:white;
                        padding:14px;
                        border-radius:10px;
                        font-size:14px;
                        line-height:1.6;
                    ">
                    ⚠️ Sorry — I couldn’t process that request right now. Please try again.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.rerun()  

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Ask a medical question about the selected PDF...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        
        if is_greeting(user_input):
            natural = (
                "Hi! 🩺😊\n\n"
                "Ask me something about the selected medical PDF — for example:\n"
                "- *Summarize this document*\n"
                "- *What are the causes mentioned?*\n"
                "- *What are the red flags?*\n"
                "- *Define important medical terms*\n\n"
                "I’ll answer strictly from the document."
            )
            st.chat_message("assistant").markdown(natural)
            st.session_state.messages.append({"role": "assistant", "content": natural})
            return

        response = ask_question(user_input, selected_pdf=st.session_state["selected_pdf"])

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")
            sources = data.get("sources", [])

            st.chat_message("assistant").markdown(answer)

            if sources:
                st.markdown("📄 **Sources:**")
                for src in sources:
                    st.markdown(f"- `{src}`")

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            
            st.markdown(
                """
                <div style="
                    background-color:#1f2933;
                    color:white;
                    padding:14px;
                    border-radius:10px;
                    font-size:14px;
                    line-height:1.6;
                ">
                ⚠️ Sorry — I couldn’t answer that right now. Please try again.
                </div>
                """,
                unsafe_allow_html=True
            )
