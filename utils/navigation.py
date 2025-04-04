import streamlit as st

def navigate(target):
    st.session_state["page"] = target
    st.rerun()
