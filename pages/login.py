import streamlit as st
import uuid
from utils.navigation import navigate

def show_login():

    st.markdown("""
        <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    

    # Init login-related state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())

    # Dummy credentials
    USER_CREDENTIALS = {
        "uwe": "lernen123",
        "gast": "abc123"
    }

    # --- Login UI ---
    if not st.session_state["logged_in"]:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("images/jonny.png", caption="Hallihallo", width=200)
        with col2:
            st.markdown("""
                <div style='text-align: center;'>
                    <h1 style='color: grey; font-size: 500%'>Mastery</h1>
                    <h1 style='color: darkviolet;'>WORTARTEN</h1>
                </div>
            """, unsafe_allow_html=True)

        st.subheader("Bitte einloggen")

        with st.form("login_form"):
            username = st.text_input("Benutzername")
            password = st.text_input("Passwort", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = username
                    st.session_state["session_id"] = str(uuid.uuid4())
                    st.session_state["chats"] = []
                    st.session_state["Wortart"] = ""
                    st.session_state["Hobby"] = ""
                    navigate("welcome")
                else:
                    st.error("Falscher Benutzername oder Passwort.")
    else:
        st.success(f"Du bist eingeloggt als {st.session_state['user']}")
        st.button("Weiter", on_click=lambda: navigate("Welcome"))
