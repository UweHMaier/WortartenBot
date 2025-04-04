import streamlit as st
from gemini_utils import generate_sentences, check_student_answer
from utils.navigation import navigate
from utils.header import show_header

def show_training():

    # --- Require login ---
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Bitte zuerst einloggen.")
        st.stop()

    # User Name and Logout in Header
    show_header() 

    # --- Page  ---
    st.title("Beim Training ...")

    # --- Check Inputs ---
    if not st.session_state["Wortart"] or not st.session_state["Hobby"]:
        st.info("Bitte zuerst deine Ziele eingeben.")
        st.stop()

    # --- Init chat-related session state keys ---
    for key, default in {
        "sentences": [],
        "sentence_index": 0,
        "student_answers": [],
        "feedbacks": [],
        "current_input": "",
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # Init full session chat history
    if "chats" not in st.session_state:
        st.session_state["chats"] = []

    # Create a new chatlog if it doesn't exist yet
    if "current_chat_id" not in st.session_state:
        import uuid
        st.session_state["current_chat_id"] = str(uuid.uuid4())
        st.session_state["chatlog"] = {
            "chat_id": st.session_state["current_chat_id"],
            "user": st.session_state["user"],
            "session_id": st.session_state["session_id"],
            "wortart": st.session_state["Wortart"],
            "hobby": st.session_state["Hobby"],
            "interactions": []
        }

    # Flag if chat already saved in chatlog
    if "chat_saved" not in st.session_state:
        st.session_state["chat_saved"] = False


    # --- Generate Gemini Sentences Once ---
    if not st.session_state["sentences"]:
        st.session_state["sentences"] = generate_sentences(
            st.session_state["Wortart"], st.session_state["Hobby"]
        )

    # --- Current Sentence Info ---
    sentences = st.session_state["sentences"]
    idx = st.session_state["sentence_index"]  #beim ersten Durchgang 0

    # --- All Sentences Done ---
    if idx >= len(sentences):
        # If current chatlog not yet saved
        if not st.session_state["chat_saved"]:
            st.session_state["chats"].append(st.session_state["chatlog"])
            st.session_state["chat_saved"] = True  # ✅ mark as saved

        st.success("Du hast alle Sätze bearbeitet.")

        # Nochmal gleiche Wortart üben; Reset everything for new chat
        st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
        if st.button(f"Nochmal die Wortart {st.session_state['Wortart']} üben"):
            for key in ["sentences", "sentence_index", "student_answers", "feedbacks", "current_input", "chatlog", "current_chat_id", "chat_saved"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # Neues Lernziel wählen
        st.write(f"Gehe zu Lernziele, um eine andere Wortart zu üben.")
        st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
        if st.button("Lernziele"):
            navigate("lernziele")

        # Zur Übersicht
        st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
        st.write(f"Deine bisherigen Trainings siehst Du bei Erfolge.")
        if st.button("Erfolge"):
            navigate("summary")

        # Stop to prevent index errors
        st.stop()


    # --- Current Sentence ---
    current = sentences[idx]
    satz = current["satz"]
    wortart = st.session_state["Wortart"]
    correct_words = current.get(wortart, []) #avoids crash if key is missing in dictionary

    # --- Display Sentence ---
    with st.chat_message("assistant"):
        st.markdown(f"**Satz {idx + 1}:** {satz}")
        st.markdown(f"Welche **{wortart}** findest du in diesem Satz?")


    # Only show input if no input is stored yet
    if st.session_state["current_input"] == "":
        with st.chat_message("user"):
            with st.form("user_input_form"):
                user_input = st.text_input("Deine Antwort ...", key=f"input_{idx}")
                submitted = st.form_submit_button("Antwort senden")

            if submitted and user_input.strip():
                st.session_state["current_input"] = user_input.strip()
                st.rerun()


    # --- If input was given, show feedback and continue button ---
    if st.session_state["current_input"] and len(st.session_state["student_answers"]) == idx:
        # are we for the first time at this sentence? Safed no answer?
        st.session_state["student_answers"].append(st.session_state["current_input"])
        feedback = check_student_answer(satz, wortart, st.session_state["current_input"], correct_words)
        # After feedback is generated store all info in state
        st.session_state["chatlog"]["interactions"].append({
            "satz": satz,
            "user_answer": st.session_state["current_input"],
            "correct_words": correct_words,
            "feedback": feedback
        })

        with st.chat_message("assistant"):
            st.markdown("**Feedback zu deiner Antwort:**")
            st.markdown(feedback)


    # Always show "Weiter" if input was already submitted
    if st.session_state["current_input"] and len(st.session_state["student_answers"]) > idx - 1:
        if st.button("Weiter zum nächsten Satz"):
            st.session_state["sentence_index"] += 1
            st.session_state["current_input"] = ""
            st.rerun()


    # Neues Lernziel wählen
    st.write(f"Oh nein, ich möchte doch eine andere Wortart üben.")
    st.markdown("""<style>div.stButton > button {background-color: #8A2BE2; color: white; font-weight: bold; border-radius: 8px; }</style>""", unsafe_allow_html=True)
    if st.button("Lernziele"):
        navigate("lernziele")