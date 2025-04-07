import streamlit as st
import pandas as pd


# Page
st.title("📊 Zusammenfassung deiner Trainingseinheiten")

# --- Check for chats ---
if "chats" not in st.session_state or len(st.session_state["chats"]) == 0:
    st.info("Du hast noch keine abgeschlossenen Chats. Gehe erst zu den Lernzielen und wähle eine Wortart.")
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

    rows.append({
        "Satz": interaction["satz"],
        "Antwort des Schülers": interaction["user_answer"],
        "Richtige Wörter": ", ".join(interaction["correct_words"]),
    })

df = pd.DataFrame(rows)

# --- Show as table ---
st.dataframe(df, use_container_width=True)

# Neues Lernziel wählen
st.write(f"Gehe zu Lernziele, um eine andere Wortart zu üben.")





