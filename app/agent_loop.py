
"""Hand-written tool-using agent for MatdarMitra."""

import re

from app.tools import qualifying_date_calculator
from app.rag import answer_question


def select_tool(question):
    """Select the appropriate tool based on user intent."""

    text = question.casefold()

    date_keywords = [
        "qualifying date",
        "turn 18",
        "turns 18",
        "18 years",
        "18th birthday",
        "when can i apply",
        "when can i register",
        "advance application",
        "eligible to register"
    ]

    has_date_intent = any(
        keyword in text for keyword in date_keywords
    )

    dob_match = re.search(
        r"\b\d{4}-\d{2}-\d{2}\b",
        question
    )

    if has_date_intent:
        if dob_match:
            return "qualifying_date_calculator", dob_match.group()

        return "ask_dob", None

    return "rag_search", None


def run_agent(question):
    """Run the agent and execute its selected tool."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    tool_name, dob = select_tool(question)

    if tool_name == "qualifying_date_calculator":
        result = qualifying_date_calculator(dob)

        return {
            "question": question,
            "selected_tool": tool_name,
            "tool_result": result,
            "answer": (
                f"You will turn 18 on {result['turns_18_on']}. "
                f"Your next qualifying date is "
                f"{result['next_qualifying_date']}. "
                f"{result['advance_application_status']} "
                f"{result['note']}"
            )
        }

    if tool_name == "ask_dob":
        return {
            "question": question,
            "selected_tool": "none",
            "answer": (
                "Please provide your date of birth in YYYY-MM-DD "
                "format so I can calculate your qualifying date."
            )
        }

    result = answer_question(question, top_k=3)

    return {
        "question": question,
        "selected_tool": "rag_search",
        **result
    }


if __name__ == "__main__":
    test_questions = [
        "When will I turn 18 and what is my qualifying date? My DOB is 2009-12-15",
        "What documents are needed with Form 6?",
        "When can I register as a voter?"
    ]

    for question in test_questions:
        print("\nQuestion:", question)

        response = run_agent(question)

        print("Selected tool:", response["selected_tool"])
        print("Answer:", response["answer"])
