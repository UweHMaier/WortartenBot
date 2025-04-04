import streamlit as st
st.set_page_config(page_title="MasteryX", layout="centered")
import uuid
from utils.navigation import navigate  # <- you create this helper

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. Init state ---
if "page" not in st.session_state:
    st.session_state["page"] = "main"

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# --- 2. Routing Logic ---
if st.session_state["page"] == "main":
    from pages.login import show_login
    show_login()

elif st.session_state["page"] == "welcome":
    from pages.welcome import show_welcome
    show_welcome()

elif st.session_state["page"] == "lernziele":
    from pages.lernziele import show_lernziele
    show_lernziele()

elif st.session_state["page"] == "training":
    from pages.training import show_training
    show_training()

elif st.session_state["page"] == "summary":
    from pages.summary import show_summary
    show_summary()

else:
    st.error("❌ Unbekannte Seite. Bitte zurück zur Startseite.")
