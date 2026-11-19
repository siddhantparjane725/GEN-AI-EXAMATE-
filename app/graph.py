
"""LangGraph agent with memory and human approval."""

from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from app.agent_loop import run_agent, select_tool


class AgentState(TypedDict, total=False):
    question: str
    selected_tool: str
    dob: str | None
    approved: bool
    answer: str
    result: dict


def choose_tool(state: AgentState):
    tool, dob = select_tool(state["question"])

    return {
        "selected_tool": tool,
        "dob": dob
    }


def approval_node(state: AgentState):
    # No approval needed when DOB is missing.
    if state["selected_tool"] == "ask_dob":
        return {"approved": False}

    decision = interrupt({
        "message": "Approve this tool execution?",
        "tool": state["selected_tool"],
        "question": state["question"],
        "dob": state.get("dob")
    })

    return {
        "approved": decision is True
    }


def execute_tool(state: AgentState):
    if state["selected_tool"] == "ask_dob":
        return {
            "answer": (
                "Please provide your date of birth "
                "in YYYY-MM-DD format."
            ),
            "result": {}
        }

    if not state.get("approved", False):
        return {
            "answer": "Tool execution was not approved.",
            "result": {}
        }

    result = run_agent(state["question"])

    return {
        "answer": result["answer"],
        "result": result
    }


builder = StateGraph(AgentState)

builder.add_node("choose_tool", choose_tool)
builder.add_node("approval", approval_node)
builder.add_node("execute_tool", execute_tool)

builder.add_edge(START, "choose_tool")
builder.add_edge("choose_tool", "approval")
builder.add_edge("approval", "execute_tool")
builder.add_edge("execute_tool", END)

# Memory persists across calls within the running process.
memory = MemorySaver()

graph = builder.compile(checkpointer=memory)


def start_agent(question, thread_id):
    config = {
        "configurable": {"thread_id": thread_id}
    }

    return graph.invoke(
        {"question": question},
        config=config
    )


def resume_agent(thread_id, approved):
    config = {
        "configurable": {"thread_id": thread_id}
    }

    return graph.invoke(
        Command(resume=approved),
        config=config
    )


if __name__ == "__main__":
    thread_id = "demo-001"

    print("Starting agent...")

    result = start_agent(
        "When will I turn 18? My DOB is 2009-12-15",
        thread_id
    )

    print("Pending approval:", result.get("__interrupt__"))

    print("\nApproving tool...")
    result = resume_agent(thread_id, True)

    print("Answer:", result.get("answer"))
