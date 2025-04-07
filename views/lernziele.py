import streamlit as st

# -- Init state ---
# Den ganzen Chatlog und die Auswahl von Wortart und Hobby löschen, falls Training abgebrochen wird
for key in ["Wortart", "Hobby", "sentences", "sentence_index", "student_answers", "feedbacks", "current_input", "chatlog", "current_chat_id", "chat_saved"]:
    if key in st.session_state:
        del st.session_state[key]

# Wortart und Hobby neu initiieren für alle Fälle
for key, default in {
    "Wortart": None,
    "Hobby": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

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
else:
    st.error("Klicke auf eine Wortart und ein Hobby!")


# Zur Übersicht
st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
st.success(f"Deine bisherigen Trainings siehst Du bei Erfolge.")

