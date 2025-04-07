import streamlit as st
import uuid

# --- Set page config ---
st.set_page_config(page_title="MasteryX", layout="centered")

# --- Init state for one session ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "user" not in st.session_state:
    st.session_state["user"] = "Demo-User"

# --- Page setup ---
lernziele_page = st.Page(
    page="views/lernziele.py",
    title="Lernziele",
    icon=":material/account_circle:",
    default=True,
)
training_page = st.Page(
    page="views/training.py",
    title="Training",
)
erfolge_page = st.Page(
    page="views/erfolge.py",
    title="Erfolge",
)

# --- Navigation Menu ---
pg = st.navigation(pages=[lernziele_page, training_page, erfolge_page])

# --- Shared on all pages ---
st.logo("images/jonny.png")
st.sidebar.markdown(f"👋 Hallo {st.session_state['user']}!")
st.sidebar.markdown(f"🆔 Session-ID: `{st.session_state['session_id']}`")

# --- Run the selected page ---
pg.run()
