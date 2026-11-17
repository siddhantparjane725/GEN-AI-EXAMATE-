
from app.agent_loop import select_tool


def test_date_question_selects_calculator():
    tool, dob = select_tool(
        "When will I turn 18? My DOB is 2009-12-15"
    )
    assert tool == "qualifying_date_calculator"
    assert dob == "2009-12-15"


def test_missing_dob_requests_dob():
    tool, dob = select_tool("When can I register as a voter?")
    assert tool == "ask_dob"
    assert dob is None


def test_form_question_selects_rag():
    tool, dob = select_tool("What documents are needed with Form 6?")
    assert tool == "rag_search"
    assert dob is None
