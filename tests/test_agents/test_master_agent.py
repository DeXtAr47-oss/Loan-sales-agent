import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from agent.master_agent import MasterAgent
from agent.workflow.state import LoanState


@pytest.fixture
def master_agent():
    return MasterAgent()

@pytest.fixture
def mock_llm():
    mock = Mock()
    mock.invoke.return_value = Mock(content="Hello! I'm here to help you with your loan application. May I know what type of loan you are looking for ?")
    return mock

@pytest.fixture
def empty_state():
    return {}

@pytest.fixture
def state_with_conversation_id():
    return {
        "conversation_id": "existing-conversation-id",
        "messages": []
    }

@pytest.fixture
def state_for_ending():
    return {
        "conversation_id": "test-conversation-id",
        "messages": [
            HumanMessage(content="I need a loan"),
            AIMessage(content="Sure I can help you with that")
        ]
    }

class TestMasterAgentInitializaiton:
    @patch('agent.master_agent.LLM')
    def test_master_agent_initilization(self, mock_llm_class):
        agent = MasterAgent()

        assert agent.llm == mock_llm_class

    @patch('agent.master_agent.LLM')
    def test_master_agent_llm_assignment(self, mock_llm_class):
        mock_llm_instance = Mock()
        mock_llm_class.return_value = mock_llm_instance

        agent = MasterAgent()

        assert agent.llm is not None

class TestMasterAgentStartConversation:
    @patch('agent.master_agent.LLM')
    def test_start_conversation_creates_new_conversation_id(self, mock_llm_class, master_agent, empty_state, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        with patch('uuid.uuid4', return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')):
            result = master_agent.start_conversation(empty_state)
        
        assert result['conversation_id'] == '12345678-1234-5678-1234-567812345678'

    @patch('agent.master_agent.LLM')
    def test_start_conversation_preserves_existing_conversation_id(self, mock_llm_class, master_agent, state_with_conversation_id, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        original_id = state_with_conversation_id['conversation_id']
        result = master_agent.start_conversation(state_with_conversation_id)

        assert result['conversation_id'] == original_id

    @patch('agent.master_agent.LLM')
    def test_start_conversation_invokes_llm_with_system_message(self, mock_llm_class, master_agent, empty_state, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        master_agent.start_conversation(empty_state)

        call_args = mock_llm.invoke.call_args[0][0]

        assert len(call_args) == 1
        assert isinstance(call_args[0], SystemMessage)
        assert "You are a friendly and professional loan sales agent, your goal is to warmly greet the customer and understood their loan requirements." in call_args[0].content

    @patch('agent.master_agent.LLM')
    def test_starts_conversation_adds_ai_message_to_state(self, mock_llm_class, master_agent, empty_state, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        result = master_agent.start_conversation(empty_state)

        assert 'messages' in result
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage) 
        assert result['messages'][0].content == mock_llm.invoke.return_value.content

    @patch('agent.master_agent.LLM')
    def test_starts_conversation_sets_next_action(self, mock_llm_class, master_agent, empty_state, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        result = master_agent.start_conversation(empty_state)

        assert result['next_action'] == 'await_customer_info'

class TestMasterAgentEndConversation:
    
    def test_conversation_rejection_status(self, master_agent, state_for_ending):
        state_for_ending['final_status'] = 'rejected'
        state_for_ending['rejection_reason'] = 'Insufficient credit score'

        result = master_agent.end_conversation(state_for_ending)

        assert len(result['messages']) == 3

        last_message = result['messages'][-1]
        assert isinstance(last_message, AIMessage)
        assert 'Unfortunately' in last_message.content
        assert 'Insufficient credit score' in last_message.content
        assert 'reapply after 3 months' in last_message.content
    
    def test_conversation_approved_status(self, master_agent, state_for_ending):
        state_for_ending['final_status'] = 'approved'
        
        result = master_agent.end_conversation(state_for_ending)

        assert len(result['messages']) == 3
        
        last_message = result['messages'][-1]
        assert isinstance(last_message, AIMessage)
        assert 'Thank you for completing your loan application' in last_message.content
        assert 'contact you shortly' in last_message.content


class TestMasterAgentIntegration:
    @patch("agent.master_agent.LLM")
    def test_complete_conversation_flow_approved(self, mock_llm_class, master_agent, empty_state, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        state = master_agent.start_conversation(empty_state)
        assert 'conversation_id' in state
        assert state['next_action'] == 'await_customer_info'

        state['messages'].append(HumanMessage(content="I need a personal loan"))
        state['messages'].append(AIMessage(content="Great! let me help you with that"))

        state['final_status'] = 'approved'
        final_state = master_agent.end_conversation(state)

        assert len(final_state['messages']) >= 3
        assert 'Thank you' in final_state['messages'][-1].content

    @patch("agent.master_agent.LLM")
    def test_complete_converation_flow_rejected(self, mock_llm_class, master_agent, empty_state, mock_llm):
        mock_llm_class.return_value = mock_llm
        master_agent.llm = mock_llm

        state = master_agent.start_conversation(empty_state)

        state['messages'].append(HumanMessage(content="I need a business loan"))
        state['messages'].append(AIMessage(content="Great! let me help you with that"))

        state['final_status'] = 'rejected'
        state['rejection_reason'] = 'High debt-to-income ratio'
        final_state = master_agent.end_conversation(state)

        assert 'Unfortunately' in final_state['messages'][-1].content
        assert 'High debt-to-income ratio' in final_state['messages'][-1].content