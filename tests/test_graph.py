
from uuid import uuid4

from app.graph import resume_agent, start_agent


def test_agent_pauses_for_approval():
    thread_id = f"test-{uuid4()}"

    result = start_agent(
        "When will I turn 18? My DOB is 2009-12-15",
        thread_id
    )

    assert "__interrupt__" in result
    assert result["selected_tool"] == "qualifying_date_calculator"


def test_agent_executes_after_approval():
    thread_id = f"test-{uuid4()}"

    start_agent(
        "When will I turn 18? My DOB is 2009-12-15",
        thread_id
    )

    result = resume_agent(thread_id, True)

    assert "2027-12-15" in result["answer"]
    assert "2028-01-01" in result["answer"]


def test_agent_stops_after_rejection():
    thread_id = f"test-{uuid4()}"

    start_agent(
        "When will I turn 18? My DOB is 2009-12-15",
        thread_id
    )

    result = resume_agent(thread_id, False)

    assert result["answer"] == "Tool execution was not approved."
