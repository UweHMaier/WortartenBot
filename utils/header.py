import streamlit as st
from utils.navigation import navigate

def show_header():
    # Only show if user is logged in
    if st.session_state.get("logged_in"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"👤 **Eingeloggt als:** {st.session_state['user']}",
                unsafe_allow_html=True
            )
        with col2:
            if st.button("🔓 Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
