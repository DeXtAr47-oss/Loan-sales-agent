import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from agent.sales_agent import SalesAgent
from agent.workflow import LoanState

class TestSalesAgent:

    @pytest.fixture(autouse = True)
    def setup(self):
        self.agent = SalesAgent()
        self.agent.llm = MagicMock()

        self.mock_response = AIMessage(content="I can offer you a loan at '10.5%' interest")
        self.agent.llm.invoke.return_value = self.mock_response

    def test_negotiate_loan_appends_ai_message(self):
        state = {
            'customer_data': {'name': 'Rahul'},
            'pre_approved_limit': 2500000,
            'messages': [HumanMessage(content='Hi, I need money for a car')],
            'loan_amount': None,
            'tenure_months': None
        }

        result = self.agent.negotiate_loan(state)

        assert len(result['messages']) == 2
        assert state['messages'][-1] == "I can offer you a loan at '10.5%' interest"
        assert state['next_action'] == 'continue_sales'

    def test_transition_to_verification(self):
        state = {
            'customer_data': {'name': 'Rahul'},
            'pre_approved_limit': 2500000,
            'messages': [],
            'loan_amount': 200000,
            'tenure_months': 24
        }

        result = self.agent.negotiate_loan(state)

        assert result['next_action'] == 'verification'

    def test_handle_empty_messages(self):
        state = {
            'customer_data': {'name': 'Rahul'},
            'pre_approved_limit': 75000,
            'messages': []
        }

        result =  self.agent.negotiate_loan(state)

        assert len(result['messages']) == 1
        self.agent.llm.invoke.assert_called_once()

    def test_system_prompt_composition(self):
        state = {
            'customer_data': {'name': 'Suresh'},
            'pre_approved_limit': 75000,
            'messages': []
        }

        self.agent.negotiate_loan(state)
        args, _ = self.agent.llm.invoke.call_args
        system_msg = args[0][0].content
        
        assert "Suresh" in system_msg
        assert "₹ 75000" in system_msg


