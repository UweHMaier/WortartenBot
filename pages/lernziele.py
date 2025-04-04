import streamlit as st
from utils.navigation import navigate
from utils.header import show_header

def show_lernziele():


    # --- Require login ---
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Bitte zuerst einloggen.")
        st.stop()

    # User Name and Logout in Header
    show_header() 

    # --- Page
    st.title("DEIN LERNZIEL")
    st.subheader("Du kannst eine Wortart mit Sätzen zu einem Lieblingsthema üben.")
    # Auswahl
    Wortarten_Auswahl = ["Nomen", "Verben", "Adjektive", "Artikel"]
    Wortart = st.pills("Welche Wortart möchtest du üben?", Wortarten_Auswahl, selection_mode="single")
    st.session_state["Wortart"] = Wortart

    Hobby_Auswahl = ["Volleyball", "Fussball", "Kino", "Schminken", "Pferde", "Rennautos", "Raumfahrt", "Musik"]
    Hobby = st.pills("Welches Thema interessiert Dich?", Hobby_Auswahl, selection_mode="single")
    st.session_state["Hobby"] = Hobby

    if Wortart and Hobby:
        st.success(f"Alles klar! Gehe zum Training und übe die Wortart **{Wortart}** mit Sätzen zum Thema **{Hobby}**.")
        if st.button("Jetzt trainieren"):
            navigate("training")
    else:
        st.error("Klicke auf eine Wortart und ein Hobby!")

    
    # Zur Übersicht
    st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
    st.success(f"Deine bisherigen Trainings siehst Du bei Erfolge.")
    if st.button("Erfolge"):
        navigate("summary")

