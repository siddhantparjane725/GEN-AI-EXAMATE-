
import json
import os
from pathlib import Path

import requests
import streamlit as st

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="MatdarMitra | Voter Assistant",
    page_icon="🗳️",
    layout="wide"
)

API_URL = os.getenv("MATDARMITRA_API", "http://127.0.0.1:8000")
FEEDBACK_FILE = Path(__file__).resolve().parent / "feedback.json"

st.markdown("""
<style>
.main-header {
    padding: 22px;
    border-radius: 14px;
    background: linear-gradient(120deg, #123B68, #2675A8);
    color: white;
    margin-bottom: 20px;
}
.main-header h1 { color: white; margin-bottom: 5px; }
.small-note { color: #64748b; font-size: 14px; }
.form-highlight {
    padding: 18px;
    border: 2px solid #2196F3;
    border-radius: 12px;
    background-color: rgba(33, 150, 243, 0.07);
}
</style>
""", unsafe_allow_html=True)


# ---------------- API HELPERS ----------------

def api_get(endpoint):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"Backend connection failed: {error}")
        return None


def api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=90
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"Request failed: {error}")
        return None


def get_records():
    data = api_get("/records?limit=100")

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return data.get("records", data.get("items", []))

    return []


def find_form_record(form_number):
    for record in get_records():
        if str(record.get("form_number", "")).strip().upper() == form_number:
            return record
    return None


# ---------------- FEEDBACK ----------------

def save_feedback(question, answer, rating):
    entry = {
        "question": question,
        "answer": answer,
        "feedback": rating
    }

    try:
        if FEEDBACK_FILE.exists():
            data = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
        else:
            data = []

        if not isinstance(data, list):
            data = []

        data.append(entry)

        FEEDBACK_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        return True

    except (OSError, json.JSONDecodeError):
        st.error("Could not save feedback.")
        return False


# ---------------- SESSION STATE ----------------

defaults = {
    "messages": [],
    "agent_thread": None,
    "agent_question": None,
    "agent_pending": False,
    "agent_approval": None,
    "wizard_result": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- HEADER ----------------

st.markdown("""
<div class="main-header">
    <h1>🗳️ MatdarMitra</h1>
    <p>Your AI-powered guide to voter registration in India.</p>
    <p>Understand forms, documents and voter-registration procedures.</p>
</div>
""", unsafe_allow_html=True)

health = api_get("/health")
if health is not None:
    st.caption("🟢 Backend connection available")
else:
    st.caption("🔴 Backend unavailable — start FastAPI to use the assistant.")


# ---------------- NAVIGATION ----------------

chat_tab, wizard_tab, about_tab = st.tabs([
    "💬 AI Assistant",
    "📋 Form Chooser",
    "ℹ️ About"
])


# ==================================================
# CHAT TAB
# ==================================================

with chat_tab:
    st.subheader("Ask MatdarMitra")
    st.write("Ask questions about voter registration, forms and documents.")

    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("citations"):
                with st.expander("📚 View source citations"):
                    for citation in message["citations"]:
                        st.write(citation)

            if message["role"] == "assistant" and message.get("question"):
                col1, col2 = st.columns(2)

                if col1.button("👍 Helpful", key=f"up_{index}") and save_feedback(
                    message["question"],
                    message["content"],
                    "positive"
):
                    st.success("Thank you for your feedback!")
                        

                if col2.button("👎 Not helpful", key=f"down_{index}") and save_feedback(
                    message["question"],
                    message["content"],
                    "negative"
):
                    st.success("Feedback saved. Thank you!")

    mode = st.radio(
        "Choose assistant mode",
        ["RAG Assistant", "AI Agent"],
        horizontal=True
    )

    question = st.chat_input("Type your voter-registration question...")

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        if mode == "RAG Assistant":
            with st.spinner("Searching official voter information..."):
                result = api_post("/ask", {"question": question})

            if result:
                answer = result.get("answer", "No answer returned.")
                citations = result.get("citations", [])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations,
                    "question": question
                })

                st.rerun()

        else:
            import uuid

            thread_id = str(uuid.uuid4())
            result = api_post("/agent", {
                "question": question,
                "thread_id": thread_id
            })

            if result:
                if result.get("status") == "approval_required":
                    st.session_state.agent_thread = thread_id
                    st.session_state.agent_question = question
                    st.session_state.agent_pending = True
                    st.session_state.agent_approval = result.get(
                        "approval_request", {}
                    )
                    st.rerun()
                else:
                    answer = result.get("answer", "No answer returned.")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "citations": [],
                        "question": question
                    })
                    st.rerun()

    # Human approval controls
    if st.session_state.agent_pending:
        st.warning("The AI agent is requesting your approval before executing a tool.")

        st.json(st.session_state.agent_approval)

        col1, col2 = st.columns(2)

        if col1.button("✅ Approve execution"):
            result = api_post("/agent", {
                "thread_id": st.session_state.agent_thread,
                "approved": True
            })

            if result:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.get("answer", ""),
                    "citations": result.get("result", {}).get("citations", []),
                    "question": st.session_state.agent_question
                })

                st.session_state.agent_pending = False
                st.rerun()

        if col2.button("❌ Reject execution"):
            result = api_post("/agent", {
                "thread_id": st.session_state.agent_thread,
                "approved": False
            })

            if result:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.get("answer", ""),
                    "citations": [],
                    "question": st.session_state.agent_question
                })

                st.session_state.agent_pending = False
                st.rerun()


# ==================================================
# FORM CHOOSER WIZARD
# ==================================================

with wizard_tab:
    st.subheader("Find the right voter-registration form")
    st.write("Answer three simple questions to get guidance.")

    with st.form("form_chooser"):
        registered = st.radio(
            "1. Are you already registered as a voter?",
            ["Yes", "No"]
        )

        moved = st.radio(
            "2. Have you moved to a different residence?",
            ["Yes", "No"]
        )

        incorrect = st.radio(
            "3. Is something incorrect on your voter card?",
            ["Yes", "No"]
        )

        submitted = st.form_submit_button(
            "Find my form",
            type="primary"
        )

    if submitted:
        if registered == "No":
            recommendation = "6"
            reason = "You indicated that you are not registered. Form 6 is used for new voter enrolment."

        elif moved == "Yes" or incorrect == "Yes":
            recommendation = "8"
            reason = "You indicated a change of residence or correction to an existing voter record. Form 8 is used for these requests."

        else:
            recommendation = None
            reason = "Based on your answers, you may not need a new application. Check your existing voter details first."

        st.session_state.wizard_result = {
            "form": recommendation,
            "reason": reason
        }

    result = st.session_state.wizard_result

    if result:
        st.divider()

        if result["form"]:
            form_number = result["form"]
            st.markdown(
                f'<div class="form-highlight"><h2>⭐ Recommended: Form {form_number}</h2>'
                f'<p>{result["reason"]}</p></div>',
                unsafe_allow_html=True
            )

            record = find_form_record(form_number)

            st.subheader("📄 Document checklist")

            if record:
                documents = record.get("documents_needed", [])

                if isinstance(documents, str):
                    documents = [
                        item.strip()
                        for item in documents.replace(";", "\n").splitlines()
                        if item.strip()
                    ]

                if documents:
                    for document in documents:
                        st.checkbox(str(document), key=f"doc_{form_number}_{document}")
                else:
                    st.info("The available record does not contain a document checklist. Please verify the current requirements with the ECI.")

                if record.get("purpose"):
                    st.write("**Purpose:**", record["purpose"])

                if record.get("source_url"):
                    st.markdown(
                        f"[View source document]({record['source_url']})"
                    )
            else:
                st.warning(
                    "The form record was not found in the backend. "
                    "Please verify the form requirements using the official ECI source."
                )

        else:
            st.info(result["reason"])

    st.caption(
        "This wizard provides preliminary guidance only. "
        "Final form selection and eligibility must be verified with the Election Commission of India."
    )


# ==================================================
# ABOUT TAB
# ==================================================

with about_tab:
    st.subheader("About MatdarMitra")

    st.write("""
    MatdarMitra is an AI-powered voter-assistance application designed
    to make voter-registration information easier to understand.

    **Technology stack**
    - Python and Streamlit
    - FastAPI
    - Retrieval-Augmented Generation (RAG)
    - Gemini Embeddings
    - ChromaDB
    - Groq LLM
    - LangGraph

    **Key capabilities**
    - Source-based voter-registration answers
    - AI agent with tool selection
    - Qualifying-date calculation
    - Human approval workflow
    - Voter-form selection wizard
    - User feedback collection
    """)
