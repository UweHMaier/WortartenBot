import streamlit as st
import uuid

# Generate unique session ID once
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())  # e.g. "f47ac10b-58cc"


# --- Dummy login credentials ---
USER_CREDENTIALS = {
    "uwe": "lernen123",
    "gast": "abc123"
}

# --- Set page config ---
st.set_page_config(page_title="Login", layout="centered")

# --- Session state init ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# --- HIDE SIDEBAR before login ---
if not st.session_state["logged_in"]:
    hide_sidebar = """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

# --- Login UI ---
if not st.session_state["logged_in"]:
    col1, col2 = st.columns([1, 2])  # image narrower than text
    with col1:
        st.image("images/jonny.png", caption="Hallihallo", width=200)
    with col2:
        st.markdown(
        """
        <div style='text-align: center;'>
            <h1 style='color: grey; font-size: 500%'>Mastery</h1>
            <h1 style='color: darkviolet;'>WORTARTEN</h1>
        </div>
        """,
        unsafe_allow_html=True)
    st.subheader("Bitte einloggen")
    
    with st.form("login_form"):
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.session_state["session_id"] = str(uuid.uuid4())  # global session ID for the login
                st.session_state["chats"] = []  # list to store multiple chat sessions
                st.session_state["Wortart"] = ""
                st.session_state["Hobby"] = ""
                st.success("Login erfolgreich!")
                st.rerun()
            else:
                st.error("Falscher Benutzername oder Passwort.")

else:
    st.title(f"Hallo, {st.session_state['user']} 👋")
    st.success("Viel Erfolg beim Üben!")
    st.write("Wähle zuerst ein Lernziel.")
    st.write("Gehe dann zum Training.")
    st.write("Feiere deine Lernerfolge.")

    # Logout in Sidebar anzeigen
    with st.sidebar:
        st.markdown(f"👤 Eingeloggt als: **{st.session_state['user']}**")
        logout = st.button("🔓 Logout")
        if logout:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
