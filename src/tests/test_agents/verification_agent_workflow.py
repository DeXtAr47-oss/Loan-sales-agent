from langchain_core.messages import HumanMessage
from src.loan_sales_agent_shared.connection import SessionLocal

from src.agent.verification_agent.verification_agent import VerificationAgent
from src.agent.states.state import LoanState

db = SessionLocal()

agent = VerificationAgent(db)
state = LoanState()

while True:

    state = agent.verify_customer(state)

    print(state["messages"][-1].content)

    user_input = input("> ")

    state["messages"].append(
        HumanMessage(content=user_input)
    )

    if state.get("customer_verified"):
        break

db.close()
