from langchain_core.messages import HumanMessage
from decimal import Decimal
from uuid import UUID, uuid4
from fastapi import UploadFile

from src.agent.states.state import LoanState
from src.loan_sales_agent_BL.schemas.chat_schema import ChatResponse, ChatRequest
from src.loan_sales_agent_shared.salary_slip_upload_helper import save_salary_slip


def make_json_safe(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dict):
        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [make_json_safe(item) for item in value]
    return value


def extract_credit_score(user):
    if not user:
        return None

    direct_credit_score = getattr(user, "credit_score", None)
    if isinstance(direct_credit_score, int):
        return direct_credit_score
    if direct_credit_score is not None:
        nested_score = getattr(direct_credit_score, "credit_score", None)
        if nested_score is not None:
            return nested_score

    credit_score_rel = getattr(user, "credit_score_rel", None)
    if credit_score_rel and getattr(credit_score_rel, "credit_score", None):
        return credit_score_rel.credit_score.credit_score

    return None


async def chat_service(
    graph,
    chat_request: ChatRequest,
    current_user,
    file: UploadFile | None = None,
):
    requested_thread_id = (chat_request.thread_id or "").strip()
    try:
        conversation_id = UUID(requested_thread_id)
    except (ValueError, TypeError, AttributeError):
        conversation_id = uuid4()

    initial_state: LoanState = {
        # Conversation
        "messages": [],
        "conversation_id": conversation_id,

        # Customer (empty initially)
        "customer_id": None,
        "customer_name": None,
        "customer_email": None,
        "customer_data": None,
        "customer_verified": False,

        # Loan details (empty initially)
        "loan_amount": Decimal("0"),
        "loan_type": "",
        "tenure_months": 0,
        "loan_offer_id": None,
        "interest_rate": Decimal("0"),
        "monthly_emi": Decimal("0"),

        # Process flags
        "kyc_verified": False,
        "credit_check_done": False,
        "under_writing_approved": False,
        "salary_slip_uploaded": False,
        "salary_slip_path": None,
        "salary_slip_date": None,
        "salary_amount": None,

        # Decision
        "pre_approved_limit": None,
        "credit_score": None,
        "application_id": None,
        "final_status": None,
        "rejection_reason": None,
        "sanction_letter_path": None,
        "sanction_letter_url": None,

        # Flow control
        "next_agent": None,
    }

    # Add user message. A file-only upload still needs a graph message so the
    # workflow can continue instead of returning the greeting branch.
    if chat_request.message.strip() or file:
        message_content = chat_request.message.strip()
        if file and not message_content:
            message_content = f"Uploaded file: {file.filename}"
        initial_state["messages"].append(
            HumanMessage(content=message_content)
        )
    else:
        return ChatResponse(
            reply="Hello! I'm your loan assistant. How can I help you today?",
            state={"conversation_id": str(initial_state["conversation_id"])}
        )

    # Use the conversation ID as LangGraph's canonical thread identifier.
    # The client sends this value back on every subsequent request.
    thread_id = str(conversation_id)

    # Populate customer data if authenticated
    if current_user:
        credit_score = extract_credit_score(current_user)
        initial_state.update({
            "customer_id": current_user.customer_id,
            "customer_name": current_user.name,
            "customer_email": current_user.email,
            "customer_data": {
                "phone": current_user.phone,
                "city": current_user.city,
                "address": current_user.address,
                "age": current_user.age,
            },
            "credit_score": credit_score,
            "customer_verified": True,
        })

    graph_config = {"configurable": {"thread_id": thread_id}}
    existing_state = await graph.aget_state(graph_config)

    upload_updates = {}
    if file:
        customer_id_for_upload = (
            current_user.customer_id
            if current_user
            else existing_state.values.get("customer_id")
        )

        if not customer_id_for_upload:
            return ChatResponse(
                reply=(
                    "Please verify your customer profile before uploading a "
                    "salary slip."
                ),
                state={"conversation_id": str(initial_state["conversation_id"])},
            )

        salary_slip_path = await save_salary_slip(customer_id_for_upload, file)
        upload_updates = {
            "salary_slip_uploaded": True,
            "salary_slip_path": salary_slip_path,
        }
        initial_state.update(upload_updates)

    # Do not overwrite values collected in earlier turns with empty defaults.
    # For an existing conversation, submit only the new message and fresh
    # authenticated-customer data; LangGraph restores the remaining state.
    graph_input = initial_state
    if existing_state.values:
        graph_input = {
            "messages": initial_state["messages"],
            "conversation_id": conversation_id,
        }
        graph_input.update(upload_updates)
        if current_user:
            graph_input.update({
                "customer_id": initial_state["customer_id"],
                "customer_name": initial_state["customer_name"],
                "customer_email": initial_state["customer_email"],
                "customer_data": initial_state["customer_data"],
                "credit_score": initial_state["credit_score"],
                "customer_verified": True,
            })

    # Invoke graph
    result = await graph.ainvoke(
        graph_input,
        config=graph_config,
    )

    # Safe extraction
    messages = result.get("messages", [])

    if not messages:
        reply = "I'm ready to help. What would you like to know about loans?"
    else:
        last = messages[-1]
        reply = getattr(last, "content", str(last))

    # Build safe state for response (exclude sensitive fields)
    safe_state = {
        "conversation_id": str(result.get("conversation_id", "")),
        "customer_id": str(result.get("customer_id")) if result.get("customer_id") else None,
        "customer_name": result.get("customer_name"),
        "customer_email": result.get("customer_email"),
        "customer_data": make_json_safe(result.get("customer_data")),
        "customer_verified": result.get("customer_verified"),
        "credit_score": result.get("credit_score"),
        "loan_type": result.get("loan_type"),
        "loan_amount": str(result.get("loan_amount")) if result.get("loan_amount") else None,
        "tenure_months": result.get("tenure_months") or None,
        "loan_offer_id": result.get("loan_offer_id"),
        "pre_approved_limit": str(result.get("pre_approved_limit")) if result.get("pre_approved_limit") else None,
        "salary_slip_uploaded": result.get("salary_slip_uploaded"),
        "salary_slip_path": result.get("salary_slip_path"),
        "salary_slip_date": result.get("salary_slip_date"),
        "salary_amount": result.get("salary_amount"),
        "application_id": result.get("application_id"),
        "monthly_emi": str(result.get("monthly_emi")) if result.get("monthly_emi") else None,
        "credit_check_done": result.get("credit_check_done"),
        "under_writing_approved": result.get("under_writing_approved"),
        "final_status": result.get("final_status"),
        "rejection_reason": result.get("rejection_reason"),
        "sanction_letter_path": result.get("sanction_letter_path"),
        "sanction_letter_url": result.get("sanction_letter_url"),
        "next_agent": result.get("next_agent"),
        "conversation_turns": len(messages),
    }

    return ChatResponse(reply=reply, state=safe_state)
