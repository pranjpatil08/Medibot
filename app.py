import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

st.set_page_config(page_title="MediBot", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
    background: linear-gradient(
        180deg,
        #111827 0%,     /* dark navy */
        #0f172a 55%,    /* slate blue */
        #0b1020 100%    /* soft charcoal */
    );
    color: #e5e7eb;
}
h1,
h1 span {
    color: #ffffff !important;
    opacity: 1 !important;
    filter: none !important;
    text-shadow: none !important;
}

header h1 {
    color: #ffffff !important;
    opacity: 1 !important;
}


div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stHeading"] h1,
div[data-testid="stHeading"] h2,
div[data-testid="stHeading"] h3,
div.stMarkdown h1,
div.stMarkdown h2,
div.stMarkdown h3 {
  color: #ffffff !important;
  opacity: 1 !important;
  filter: none !important;
  text-shadow: none !important;
}

div[data-testid="stMarkdown"] h1,
div[data-testid="stMarkdown"] h2,
div[data-testid="stMarkdown"] h3 {
  color: #ffffff !important;
  opacity: 1 !important;
  filter: none !important;
}

div[data-testid="stMarkdownContainer"] svg,
div[data-testid="stHeading"] svg,
div[data-testid="stMarkdown"] svg {
  color: #ffffff !important;
  fill: #ffffff !important;
  opacity: 1 !important;
  filter: none !important;
}

div[data-testid="stMarkdownContainer"],
div[data-testid="stHeading"],
div[data-testid="stMarkdown"] {
  opacity: 1 !important;
  filter: none !important;
}


    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08172e, #0b1f3a);
        border-right: 1px solid #1e3a8a;
    }

    section[data-testid="stSidebar"] * {
        color: #cfe7ff !important;
    }

    
    h1, h2, h3 {
        color: #1e293b !important;   
        font-weight: 800 !important;
    }

    
    div[data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #0f1e35, #12264a);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid #1e40af;
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    }

    
    div[data-testid="stChatMessage"][aria-label="assistant"] {
        border-left: 4px solid #38bdf8;
        background: linear-gradient(135deg, #0f2a44, #143b66);
    }

    
    div[data-testid="stChatMessage"][aria-label="user"] {
        border-left: 4px solid #2563eb;
        background: linear-gradient(135deg, #0b1f3a, #102a4c);
    }

    
    div[data-testid="stChatInput"] textarea {
        background-color: #0b1f3a !important;
        color: #e5f0ff !important;
        border-radius: 14px !important;
        border: 1px solid #2563eb !important;
        padding: 14px !important;
        font-size: 15px !important;
        min-height: 52px !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #9ac7ff !important;
    }

    div[data-testid="stChatInput"] textarea:focus {
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56,189,248,0.35) !important;
    }

    
    button {
        border-radius: 12px !important;
        border: 1px solid #2563eb !important;
        background: linear-gradient(135deg, #0b1f3a, #102a4c) !important;
        color: #e0f2fe !important;
        font-weight: 500;
    }

    button:hover {
        background: linear-gradient(135deg, #102a4c, #143b66) !important;
        border-color: #38bdf8 !important;
        color: #e0f2fe !important;
    }

    
    div[data-baseweb="select"] > div {
        background-color: #0b1f3a !important;
        border: 1px solid #2563eb !important;
        border-radius: 12px !important;
        color: #e5f0ff !important;
    }

    /* ---------- Source Tags ---------- */
    code {
        background: #0f2a44;
        color: #7dd3fc;
        border-radius: 8px;
        padding: 4px 8px;
        font-size: 13px;
        border: 1px solid #1e40af;
    }

   
    div[data-testid="stAlert"]{
        background: #fff7d6 !important;
        border: 1px solid #fbbf24 !important;
        border-radius: 16px !important;
    }
    div[data-testid="stAlert"] *{
        color: #1e293b !important;
        font-weight: 600;
    }

    
    
    div[data-testid="stInfo"]{
        background: #eafaf1 !important;        
        border: 1px solid #34d399 !important;  
        border-radius: 16px !important;
    }

    div[data-testid="stInfo"] *{
        color: #065f46 !important;             /* dark green text */
        font-weight: 600;
    }

    
    div[data-baseweb="select"] > div {
        background: linear-gradient(180deg, #1e3a8a, #1e40af) !important;
        border: 1px solid #60a5fa !important;
        color: #ffffff !important;
        font-weight: 600;
    }

    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }

    /* ===== Fix "Medical Actions (one-click)" expander header ===== */
    div[data-testid="stExpander"] > details > summary {
        background: linear-gradient(180deg, #1e293b, #111827) !important;
        color: #e5f0ff !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-weight: 700 !important;
    }

    /* Expander icon */
    div[data-testid="stExpander"] summary svg {
        color: #93c5fd !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("🩺 MediBot")
st.caption("A medical document assistant that answers strictly from your uploaded PDFs.")

st.warning(
    "⚠️ **Medical disclaimer:** I’m not a doctor. I can summarize and explain your uploaded medical PDFs, "
    "but I can’t diagnose or replace professional medical advice. If you have severe symptoms or an emergency, "
    "seek urgent medical care."
)

render_uploader()
render_chat()
render_history_download()
