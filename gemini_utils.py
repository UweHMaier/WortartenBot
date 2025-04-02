# gemini_utils.py
import google.generativeai as genai
import streamlit as st
import os
import json
import re
from dotenv import load_dotenv

# Load the API key once
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Init model once
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_sentences(Wortart: str, Hobby: str) -> list:
    """
    Sends a prompt to Gemini, gets structured JSON response,
    and stores it in st.session_state["sentences"]
    """
    if not Wortart or not Hobby:
        return []

    prompt = (
        f"Erstelle 5 Sätze zum Thema {Hobby}. Jeder Satz soll mindestens ein Wort der Wortart {Wortart} enthalten. "
        f"Gib die Antwort als JSON-Liste mit folgendem Format zurück:\n"
        f"[\n"
        f"{{\"satz\": \"...\", \"{Wortart}\": [\"wort1\"]}},\n"
        f"  ...\n"
        f"]\n"
        f"Gib nur gültiges JSON zurück, ohne Einleitung oder Text."
    )

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            bot_response = json.loads(json_str)

            # Save in session state
            st.session_state["sentences"] = bot_response
            return bot_response
        else:
            st.warning("Keine gültige JSON-Antwort erhalten.")
            return []

    except Exception as e:
        st.error(f"Fehler bei Gemini: {e}")
        return []
    


def check_student_answer(sentence: str, wortart: str, student_input: str, correct_list: list) -> str:
    """
    Sends student's answer and sentence to Gemini. Asks Gemini to evaluate
    whether their response matches the correct words of the given word class.
    """
    correct_words_formatted = ", ".join(correct_list)

    prompt = (
        f"Hier ist ein deutscher Satz:\n\n"
        f"\"{sentence}\"\n\n"
        f"Die Ziel-Wortart ist: {wortart}.\n"
        f"Der Schüler hat folgende Wörter als {wortart} angegeben: {student_input}.\n\n"
        f"Bewerte die Antwort des Schülers:\n"
        f"- Welche Wörter sind korrekt erkannte {wortart}?\n"
        f"- Welche sind falsch und warum?\n"
        f"Akzeptiere eine Wortart auch bei kleinen Schreibfehlern. Melde das aber zurück."
        f"Schreibe eine kurze Rückmeldung auf Deutsch für den Schüler."
        f"Spreche den Schüler direkt und personlich an mit Du."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Fehler bei der Rückmeldung: {e}"
