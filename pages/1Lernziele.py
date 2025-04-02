import streamlit as st

# Page init ----
st.set_page_config(
    page_title="Lernziele",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Require login ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Bitte zuerst einloggen.")
    st.stop()

# Logout in Sidebar anzeigen
with st.sidebar:
    st.markdown(f"👤 Eingeloggt als: **{st.session_state['user']}**")
    logout = st.button("🔓 Logout")
    if logout:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- Page
st.title("DEINE LERNZEIEL")
st.header("Was möchtest Du üben?")

# Auswahl
Wortarten_Auswahl = ["Nomen", "Verben", "Adjektive", "Artikel"]
Wortart = st.pills("Welche Wortart willst Du üben?", Wortarten_Auswahl, selection_mode="single")
st.session_state["Wortart"] = Wortart

Hobby_Auswahl = ["Volleyball", "Fussball", "Kino", "Schminken", "Pferde"]
Hobby = st.pills("Was interessiert Dich?", Hobby_Auswahl, selection_mode="single")
st.session_state["Hobby"] = Hobby

if Wortart and Hobby:
    st.success(f"Du übst jetzt die Wortart {Wortart} mit Sätzen zum Thema {Hobby}.")
    st.write("Gehe zum Training!")
else:
    st.error("Klicke auf eine Wortart und ein Hobby!")

