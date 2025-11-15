import streamlit as st
import pandas as pd
import random

# --- Helper function to load a quiz ---
@st.cache_data
def load_quiz(file):
    return pd.read_csv(file)

# --- Main ---
st.set_page_config(page_title="Locked in Pookie Quiz", page_icon="🧠", layout="centered")
st.title("Super Akaesha Lock in Quiz")

# Sidebar for selecting quiz
quiz_choice = st.sidebar.selectbox(
    "Choose a quiz topic:",
    [
        "T Cell Biology",
        "Bacterial Infections",
        "B Cell Biology",
        "Antiviral Immunity",
        "Antibiotics",
        "Antivirals",
        "Immune Diseases",
        "Infection and Disease"
    ]
)

quiz_emojis = {
    "T Cell Biology": "🧬",
    "Bacterial Infections": "🦠",
    "B Cell Biology": "💉",
    "Antiviral Immunity": "🛡️",
    "Antibiotics": "💊",
    "Antivirals": "💊",
    "Immune Diseases": "🧪",
    "Infection and Disease": "🧫"
}


st.subheader(f"Current Quiz: {quiz_choice} {quiz_emojis.get(quiz_choice, '')}")

quiz_files = {
    "T Cell Biology": "t_cell_biology_quiz.csv",
    "Bacterial Infections": "Bacterial_Infections_Quiz.csv",
    "B Cell Biology": "b_cell_quiz.csv",
    "Antiviral Immunity": "antiviral_immunity_quiz.csv",
    "Antibiotics": "antibiotics_quiz.csv",
    "Antivirals": "antivirals_quiz.csv",
    "Immune Diseases": "immune_diseases_quiz.csv",
    "Infection and Disease": "infection_and_disease_quiz.csv"
}


df = load_quiz(quiz_files[quiz_choice])

# --- Initialize session state ---
if "questions" not in st.session_state or st.session_state.get("last_quiz") != quiz_choice:
    st.session_state.questions = df.sample(frac=1).reset_index(drop=True)
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.last_quiz = quiz_choice
    st.session_state.answered = False
    st.session_state.completed = False
    st.session_state.shuffled_options = {}
    st.session_state.selected_answers = {}

questions = st.session_state.questions

# --- Quiz complete ---
if st.session_state.q_index >= len(questions):
    if not st.session_state.completed:
        st.balloons()
        st.session_state.completed = True
        
    st.header(f"🎉 Quiz Complete! Your score: {st.session_state.score}/{len(questions)}")

    # Calculate percentage
    score_pct = st.session_state.score / len(questions) * 100

    # Funny reward message if over 50%
    if score_pct >= 50:
        st.markdown("🎟️ **Ticket earned! Redeem 10 minutes of Reels time!** 😎")
        # Example: Add a fun GIF or emoji animation
        st.image("https://media.tenor.com/M1DL4uWPX8AAAAAM/cat-cute.gif", width=300)
    else:
        st.markdown("😢 Better luck next time! No Reels for pookie.")

    if st.button("Restart Quiz"):
        st.session_state.questions = df.sample(frac=1).reset_index(drop=True)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.completed = False
        st.session_state.shuffled_options = {}
        st.session_state.selected_answers = {}
else:
    # --- Display current question ---
    q = questions.iloc[st.session_state.q_index]
    st.markdown(f"📝 Question {st.session_state.q_index + 1}/{len(questions)}")
    st.write(q["Question"])

    # Shuffle options once per question
    if st.session_state.q_index not in st.session_state.shuffled_options:
        options = ["Option A", "Option B", "Option C", "Option D"]
        random.shuffle(options)
        st.session_state.shuffled_options[st.session_state.q_index] = options
    else:
        options = st.session_state.shuffled_options[st.session_state.q_index]

    # Load previous selection if any
    default_selection = st.session_state.selected_answers.get(st.session_state.q_index, None)

    # --- Form for selecting answer ---
    with st.form(key=f"form{st.session_state.q_index}"):
        selected_answer = st.radio(
            "Select your answer:",
            [q[o] for o in options],
            index=[q[o] for o in options].index(default_selection) if default_selection else 0
        )
        st.session_state.selected_answers[st.session_state.q_index] = selected_answer
        submitted = st.form_submit_button("Submit Answer")

    # --- Handle submission ---
    if submitted and not st.session_state.answered:
        st.session_state.answered = True
        if selected_answer == q["Correct Answer"]:
            st.session_state.score += 1
            st.success("✅ Good job pookie!")
        else:
            st.error(f"❌ Nice try pookie! Correct answer: {q['Correct Answer']}")

    # --- Next Question button ---
    if st.session_state.answered:
        if st.button("Next Question"):
            st.session_state.q_index += 1
            st.session_state.answered = False
