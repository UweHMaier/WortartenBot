import streamlit as st
from utils.navigation import navigate
from utils.header import show_header

def show_welcome():
    # User Name and Logout in Header
    show_header() 

    st.title("🎉 Willkommen!")
    st.write("Schön, dass du da bist.")

    if st.button("Weiter zu deinen Zielen"):
        navigate("lernziele")
