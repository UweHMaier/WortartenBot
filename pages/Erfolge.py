import streamlit as st
import pandas as pd

# Page init ----
st.set_page_config(
    page_title="Meine Lernerfolge",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Require login ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Bitte zuerst einloggen.")
    st.stop()

# --- Sidebar Logout ---
with st.sidebar:
    st.markdown(f"👤 Eingeloggt als: **{st.session_state['user']}**")
    if st.button("🔓 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Page
st.title("📊 Zusammenfassung deiner Trainingseinheiten")

# --- Check for chats ---
if "chats" not in st.session_state or len(st.session_state["chats"]) == 0:
    st.info("Du hast noch keine abgeschlossenen Chats.")
    st.stop()

# --- Choose chat session to view ---
session_ids = [f"{i+1}. Chat ({chat['wortart']} / {chat['hobby']})" for i, chat in enumerate(st.session_state["chats"])]
selected = st.selectbox("Wähle ein Training aus", options=range(len(session_ids)), format_func=lambda i: session_ids[i])
chat = st.session_state["chats"][selected]

# --- Prepare DataFrame from interactions ---
rows = []
for i, interaction in enumerate(chat["interactions"]):
    correct = set(word.lower() for word in interaction["correct_words"])
    student = set(word.strip().lower() for word in interaction["user_answer"].split(","))
    correct_found = correct.intersection(student)

    rows.append({
        "Satz": interaction["satz"],
        "Antwort des Schülers": interaction["user_answer"],
        "Richtige Wörter": ", ".join(interaction["correct_words"]),
    })

df = pd.DataFrame(rows)

# --- Show as table ---
st.dataframe(df, use_container_width=True)




