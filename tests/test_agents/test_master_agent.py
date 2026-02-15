import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

from agent.master_agent import MasterAgent


# --- Mock LLM response object ---
class MockResponse:
    def __init__(self, content):
        self.content = content


@pytest.fixture
def mock_llm(monkeypatch):
    mock = MagicMock()
    mock.invoke.return_value = MockResponse("Hello! How can I help you today?")

    # patch MODEL inside the module
    monkeypatch.setattr("agent.master_agent.MODEL", mock)
    return mock


@pytest.fixture
def agent(mock_llm):
    return MasterAgent()


# --- Test start_conversation ---
def test_start_conversation_initializes_state(agent):
    state = {}

    result = agent.start_conversation(state)

    assert "conversation_id" in result
    assert result["next_action"] == "await_customer_info"
    assert isinstance(result["messages"][0], AIMessage)
    assert "Hello!" in result["messages"][0].content


# --- Test start_conversation preserves existing conversation_id ---
def test_start_conversation_keeps_existing_id(agent):
    state = {"conversation_id": "existing-id"}

    result = agent.start_conversation(state)

    assert result["conversation_id"] == "existing-id"


# --- Test end_conversation approved ---
def test_end_conversation_approved(agent):
    state = {
        "final_status": "approved",
        "messages": []
    }

    result = agent.end_conversation(state)

    assert len(result["messages"]) == 1
    assert "Thank you for completing your loan" in result["messages"][0].content


# --- Test end_conversation rejected ---
def test_end_conversation_rejected(agent):
    state = {
        "final_status": "rejected",
        "rejection_reason": "Low credit score",
        "messages": []
    }

    result = agent.end_conversation(state)

    # rejected branch does NOT append message in your code
    assert result["messages"] == []
