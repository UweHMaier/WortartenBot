import streamlit as st
import pandas as pd
from utils.navigation import navigate
from utils.header import show_header

def show_summary():

    # --- Require login ---
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Bitte zuerst einloggen.")
        st.stop()

    # User Name and Logout in Header
    show_header() 

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
        st.info("Du hast noch keine abgeschlossenen Chats. Gehe erst zu den Lernzielen und wähle eine Wortart.")
        st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
        if st.button("Lernziele"):
            navigate("lernziele")
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

    # Neues Lernziel wählen
    st.write(f"Gehe zu Lernziele, um eine andere Wortart zu üben.")
    st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
    if st.button("Lernziele"):
        navigate("lernziele")




