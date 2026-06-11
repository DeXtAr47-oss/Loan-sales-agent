from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from src.agent.states.state import LoanState
from src.loan_sales_agent_shared.config import LLM
from src.loan_sales_agent_DL.repository.customer_repository import get_customer_by_email

class VerificationAgent:
    def __init__(self, db):
        self.llm = LLM
        self.db = db
    
    def verify_customer(self, state: LoanState) -> LoanState:
        messages = state.get("messages", [])
 
        # ── Step 1: Check if we already asked for email ──────────────────────
        # Look back through messages to see if the agent has already asked for email
        already_asked = any(
            isinstance(msg, AIMessage) and "email" in msg.content.lower()
            for msg in messages
        )
 
        # ── Step 2: Haven't asked yet — ask for email and wait ───────────────
        if not already_asked:
            system_msg = """You are a verification agent. Ask the customer to provide 
            their email address to verify their identity."""
            response = self.llm.invoke([SystemMessage(content=system_msg)])
            state["messages"].append(response)
            state["customer_verified"] = False
            return state
 
        # ── Step 3: Already asked — extract email from latest human message ──
        # Find the last HumanMessage after our email-ask
        last_human_msg = next(
            (msg for msg in reversed(messages) if isinstance(msg, HumanMessage)),
            None
        )
 
        if not last_human_msg:
            # Asked but no human reply yet — do nothing and wait
            return state
 
        # ── Step 4: Use LLM to extract email from the user's reply ───────────
        extraction_prompt = f"""Extract the email address from the following message.
        Return ONLY the email address with no extra text. If no valid email is found, return 'NOT_FOUND'.
 
        Message: {last_human_msg.content}"""
 
        extraction_response = self.llm.invoke([SystemMessage(content=extraction_prompt)])
        extracted_email = extraction_response.content.strip()
 
        # ── Step 5: No valid email in reply — ask again ──────────────────────
        if extracted_email == "NOT_FOUND" or "@" not in extracted_email:
            retry_msg = """I couldn't find a valid email address in your message. 
            Could you please provide your registered email address?"""
            state["messages"].append(AIMessage(content=retry_msg))
            state["customer_verified"] = False
            return state
 
        # ── Step 6: Query the database ───────────────────────────────────────
        customer = get_customer_by_email(self.db, extracted_email)
 
        # ── Step 7a: Customer found ───────────────────────────────────────────
        if customer:
            state["customer_verified"] = True
            state["customer_id"] = customer.id
            state["customer_name"] = customer.name
            state["customer_data"] = {
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address,
                "city": customer.city,
                "age": customer.age,
                "current_loan_amount": customer.current_loan_amount,
                "pre_approved_limit": customer.pre_approved_limit,
            }
            state["next_action"] = "kyc"
 
            confirmation_msg = f"""Email Verified Successfully
 
Welcome back, {customer.name}! Your identity has been confirmed.
We will now proceed with your KYC verification."""
            state["messages"].append(AIMessage(content=confirmation_msg))
 
        # ── Step 7b: Customer not found ──────────────────────────────────────
        else:
            state["customer_verified"] = False
            state["next_action"] = "verification_failed"
 
            not_found_msg = f"""I was unable to find an account associated with 
            '{extracted_email}'. Please check your email and try again, or contact 
            support if you believe this is an error."""
            state["messages"].append(AIMessage(content=not_found_msg))
 
        return state
    
    def verify_kyc(self, state: LoanState) -> LoanState:
        customer_data = state.get("customer_data", {})
        
        if customer_data:
            state["kyc_verified"] = True
            verification_msg = f"""✓ KYC Verification Complete
            
Name: {customer_data['name']}
Phone: {customer_data['phone']}
Address: {customer_data['address']}
City: {customer_data['city']}

All details verified successfully from our CRM system."""
            
            state["messages"].append(AIMessage(content=verification_msg))
            state["next_action"] = "underwriting"
        else:
            state["kyc_verified"] = False
            state["next_action"] = "kyc_failed"
        
        return state
