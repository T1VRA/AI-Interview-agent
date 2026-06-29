import streamlit as st

from retrieval import load_dataset
from speech_to_text import transcribe_audio
from llm import evaluate_answer, generate_summary
from text_to_speech import generate_audio

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Voice Interview Agent",
    page_icon="🎤",
    layout="wide"
)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

dataset = load_dataset()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "results" not in st.session_state:
    st.session_state.results = []

if "waiting_continue" not in st.session_state:
    st.session_state.waiting_continue = False

if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🎤 AI Voice Interview Agent")

st.caption(
    "Whisper • Gemini • Google TTS"
)

# ---------------------------------------------------
# START SCREEN
# ---------------------------------------------------

if not st.session_state.started:

    st.markdown("## Welcome!")

    st.write(
        """
This interview contains **10 Machine Learning questions**.

Each question will be evaluated by Gemini.

Your feedback will include:

- Score
- Strengths
- Weaknesses
- Ideal Answer
- Follow-up Question

At the end you'll receive an overall interview summary.
"""
    )

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        st.session_state.started = True

        st.rerun()

    st.stop()

# ---------------------------------------------------
# INTERVIEW COMPLETE
# ---------------------------------------------------

if st.session_state.interview_complete:

    st.success("🎉 Interview Completed")

    summary = generate_summary(
        st.session_state.results
    )

    st.markdown(summary)

    audio = generate_audio(summary)

    st.audio(audio)

    st.stop()

# ---------------------------------------------------
# PROGRESS
# ---------------------------------------------------

progress = (
    st.session_state.current_question
) / len(dataset)

st.progress(progress)

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

for item in st.session_state.chat_history:

    with st.chat_message(item["role"]):

        st.markdown(item["content"])

        if item.get("audio"):

            st.audio(item["audio"])

# ---------------------------------------------------
# CURRENT QUESTION
# ---------------------------------------------------

question = dataset[
    st.session_state.current_question
]

if not st.session_state.waiting_continue:

    with st.chat_message("assistant"):

        st.markdown(
            f"""
### Question {st.session_state.current_question+1}/{len(dataset)}

{question["question"]}
"""
        )

    audio = st.audio_input(
        "🎤 Record your answer"
    )

    if audio:

        with st.spinner(
            "Transcribing..."
        ):

            transcript = transcribe_audio(audio)

        with st.spinner(
            "Evaluating..."
        ):

            feedback = evaluate_answer(

                question["question"],

                question["ideal_answer"],

                transcript

            )

        feedback_audio = generate_audio(
            feedback
        )

        st.session_state.chat_history.append(

            {
                "role":"assistant",
                "content":
f"""
### Question

{question["question"]}
"""
            }

        )

        st.session_state.chat_history.append(

            {
                "role":"user",
                "content":
f"""
### Your Answer

{transcript}
"""
            }

        )

        st.session_state.chat_history.append(

            {
                "role":"assistant",

                "content":
f"""
### Feedback

{feedback}
""",

                "audio":feedback_audio

            }

        )

        st.session_state.results.append(

            {

                "question":
question["question"],

                "ideal_answer":
question["ideal_answer"],

                "candidate_answer":
transcript,

                "feedback":
feedback

            }

        )

        st.session_state.waiting_continue = True

        st.rerun()
        
# ---------------------------------------------------
# WAIT FOR USER TO CONTINUE
# ---------------------------------------------------

else:

    st.divider()

    if st.button(
        "➡ Continue Interview",
        use_container_width=True
    ):

        st.session_state.waiting_continue = False

        st.session_state.current_question += 1

        # Finished all questions
        if (
            st.session_state.current_question
            >= len(dataset)
        ):

            st.session_state.interview_complete = True

        st.rerun()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("Interview Progress")

    st.metric(
        "Questions Completed",
        f"{st.session_state.current_question}/{len(dataset)}"
    )

    st.progress(
        st.session_state.current_question
        / len(dataset)
    )

    st.divider()

    st.subheader("Project Stack")

    st.markdown(
        """
- 🎤 Browser Audio
- 🧠 Whisper
- 🤖 Gemini
- 🔊 Google TTS
- 🌐 Streamlit
"""
    )

    st.divider()

    if st.button(
        "🔄 Restart Interview",
        use_container_width=True
    ):

        st.session_state.started = False

        st.session_state.current_question = 0

        st.session_state.chat_history = []

        st.session_state.results = []

        st.session_state.waiting_continue = False

        st.session_state.interview_complete = False

        st.rerun()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Built using Whisper • Gemini • Streamlit • Google Text-to-Speech"
)