import re
import uuid
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from langchain_community.tools import tool
from langchain_core.messages import AIMessage
from pypdf import PdfReader

from src.agent.states.state import LoanState
from src.loan_sales_agent_DL.models.loan_application_model import (
    LoanApplication,
    RelLoanApplicationCustomer,
)
from src.loan_sales_agent_DL.repository.loan_application_repository import (
    get_active_loan_application_by_customer_id,
)
from src.loan_sales_agent_shared.config import (
    EMBEDDING_MODEL,
    EMI_TO_SALARY_RATIO,
    INDEX,
    MIN_CREDIT_SCORE,
)
from src.loan_sales_agent_shared.connection import AsyncSessionLocal


def _extract_text_from_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        return ""

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    return path.read_text(encoding="utf-8", errors="ignore").strip()


def _parse_salary_slip_date(text: str) -> date | None:
    date_patterns = (
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        r"\b([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4})\b",
        r"\b(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})\b",
        r"\b([A-Za-z]{3,9}\s+\d{4})\b",
    )
    date_formats = (
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%B %d %Y",
        "%B %d, %Y",
        "%b %d %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
        "%B %Y",
        "%b %Y",
    )

    for pattern in date_patterns:
        for match in re.findall(pattern, text):
            normalized_match = match.replace(",", "")
            for date_format in date_formats:
                try:
                    parsed = datetime.strptime(normalized_match, date_format).date()
                    return parsed
                except ValueError:
                    continue

    return None


def _parse_monthly_salary(text: str) -> Decimal | None:
    salary_patterns = (
        r"(?:net\s+pay|net\s+salary|monthly\s+salary|gross\s+salary|salary)\D{0,30}"
        r"(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d{1,2})?)",
    )

    for pattern in salary_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return Decimal(match.group(1).replace(",", ""))

    return None


def _is_less_than_six_months_old(slip_date: date) -> bool:
    today = date.today()
    month_delta = (
        (today.year - slip_date.year) * 12
        + today.month
        - slip_date.month
    )
    return month_delta < 6


def _calculate_emi(
    loan_amount: Decimal,
    annual_interest_rate: Decimal,
    tenure_months: int,
) -> Decimal:
    if tenure_months <= 0:
        return Decimal("0")

    monthly_rate = annual_interest_rate / Decimal("1200")
    if monthly_rate == 0:
        return loan_amount / Decimal(tenure_months)

    rate_factor = (Decimal("1") + monthly_rate) ** tenure_months
    emi = loan_amount * monthly_rate * rate_factor / (rate_factor - Decimal("1"))
    return emi.quantize(Decimal("0.01"))


async def _save_underwriting_decision(
    customer_id: str,
    conversation_id: str,
    loan_amount: Decimal,
    tenure_months: int,
    interest_rate: Decimal,
    monthly_emi: Decimal,
    status: str,
    rejection_reason: str | None,
) -> int:
    async with AsyncSessionLocal() as db:
        customer_uuid = uuid.UUID(str(customer_id))
        active_application = await get_active_loan_application_by_customer_id(
            db,
            customer_uuid,
        )

        if active_application:
            active_application.conversation_id = conversation_id
            active_application.loan_amount = loan_amount
            active_application.tenure_months = tenure_months
            active_application.interest_rate = interest_rate
            active_application.monthly_emi = int(monthly_emi)
            active_application.status = status
            active_application.rejection_reason = rejection_reason
            await db.commit()
            await db.refresh(active_application)
            return active_application.application_id

        new_application = LoanApplication(
            conversation_id=conversation_id,
            conversation_history="",
            loan_amount=loan_amount,
            tenure_months=tenure_months,
            interest_rate=interest_rate,
            monthly_emi=int(monthly_emi),
            status=status,
            rejection_reason=rejection_reason,
            is_deleted=False,
        )
        db.add(new_application)
        await db.flush()

        db.add(
            RelLoanApplicationCustomer(
                application_id=new_application.application_id,
                customer_id=customer_uuid,
                is_deleted=False,
            )
        )
        await db.commit()
        await db.refresh(new_application)
        return new_application.application_id


@tool
async def process_salary_slip_tool(
    customer_id: str,
    salary_slip_path: str,
):
    """
    Extract salary-slip text, embed it, store it in Pinecone, retrieve it back,
    and return the slip date plus monthly salary.
    """
    slip_text = _extract_text_from_file(salary_slip_path)
    if not slip_text:
        return {
            "success": False,
            "error": "Could not extract text from the uploaded salary slip.",
        }

    embedding = await EMBEDDING_MODEL.aembed_query(slip_text)
    vector_id = f"salary-slip-{customer_id}-{datetime.utcnow().timestamp()}"
    metadata = {
        "customer_id": str(customer_id),
        "document_type": "salary_slip",
        "salary_slip_path": salary_slip_path,
        "text": slip_text[:3000],
        "created_at": datetime.utcnow().isoformat(),
    }

    INDEX.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": embedding,
                "metadata": metadata,
            }
        ]
    )

    query_result = INDEX.query(
        vector=embedding,
        top_k=1,
        include_metadata=True,
        filter={
            "customer_id": {"$eq": str(customer_id)},
            "document_type": {"$eq": "salary_slip"},
        },
    )

    matches = getattr(query_result, "matches", None)
    if matches is None and hasattr(query_result, "get"):
        matches = query_result.get("matches", [])
    matches = matches or []
    if not matches:
        return {
            "success": False,
            "error": "Salary slip was stored but could not be retrieved from Pinecone.",
        }

    top_match = matches[0]
    metadata = getattr(top_match, "metadata", None)
    if metadata is None and hasattr(top_match, "get"):
        metadata = top_match.get("metadata", {})
    metadata = metadata or {}
    retrieved_text = metadata.get("text", "")
    slip_date = _parse_salary_slip_date(retrieved_text)
    monthly_salary = _parse_monthly_salary(retrieved_text)

    return {
        "success": True,
        "vector_id": (
            getattr(top_match, "id", None)
            if getattr(top_match, "id", None) is not None
            else top_match.get("id") if hasattr(top_match, "get") else None
        ),
        "salary_slip_date": slip_date.isoformat() if slip_date else None,
        "salary_slip_is_recent": (
            _is_less_than_six_months_old(slip_date)
            if slip_date
            else False
        ),
        "salary_amount": str(monthly_salary) if monthly_salary else None,
    }


@tool
async def evaluate_underwriting_decision_tool(
    customer_id: str,
    conversation_id: str,
    loan_amount: str,
    pre_approved_limit: str,
    tenure_months: int,
    credit_score: int,
    salary_amount: str | None = None,
    interest_rate: str = "9.5",
):
    """
    Apply underwriting rules and persist the loan application decision.

    Rules:
    1. loan_amount <= pre_approved_limit: approve instantly
    2. loan_amount <= 2 * pre_approved_limit: require salary slip and approve
       only when EMI <= 50% of salary
    3. reject when loan_amount > 2 * pre_approved_limit or credit_score < 700
    """
    loan_amount_decimal = Decimal(str(loan_amount))
    pre_approved_limit_decimal = Decimal(str(pre_approved_limit))
    interest_rate_decimal = Decimal(str(interest_rate or "9.5"))
    monthly_emi = _calculate_emi(
        loan_amount_decimal,
        interest_rate_decimal,
        tenure_months,
    )

    status = "rejected"
    rejection_reason = None
    requires_salary_slip = False

    if credit_score < MIN_CREDIT_SCORE:
        rejection_reason = (
            f"Credit score {credit_score} is below the minimum requirement "
            f"of {MIN_CREDIT_SCORE}."
        )
    elif loan_amount_decimal <= pre_approved_limit_decimal:
        status = "approved"
    elif loan_amount_decimal <= Decimal("2") * pre_approved_limit_decimal:
        requires_salary_slip = True
        if salary_amount is None:
            return {
                "status": "pending_salary_slip",
                "requires_salary_slip": True,
                "monthly_emi": str(monthly_emi),
                "rejection_reason": None,
                "application_id": None,
            }

        salary_decimal = Decimal(str(salary_amount))
        if monthly_emi <= Decimal(str(EMI_TO_SALARY_RATIO)) * salary_decimal:
            status = "approved"
        else:
            rejection_reason = (
                f"Expected EMI ₹{monthly_emi:,.2f} exceeds 50% of monthly "
                f"salary ₹{salary_decimal:,.2f}."
            )
    else:
        rejection_reason = (
            f"Loan amount ₹{loan_amount_decimal:,.2f} exceeds 2x the "
            f"pre-approved limit ₹{pre_approved_limit_decimal:,.2f}."
        )

    application_id = await _save_underwriting_decision(
        customer_id=customer_id,
        conversation_id=conversation_id,
        loan_amount=loan_amount_decimal,
        tenure_months=tenure_months,
        interest_rate=interest_rate_decimal,
        monthly_emi=monthly_emi,
        status=status,
        rejection_reason=rejection_reason,
    )

    return {
        "status": status,
        "requires_salary_slip": requires_salary_slip,
        "monthly_emi": str(monthly_emi),
        "rejection_reason": rejection_reason,
        "application_id": application_id,
    }


class UnderwritingAgent:
    def _get_interest_rate(self, state: LoanState) -> Decimal:
        interest_rate = state.get("interest_rate") or Decimal("0")
        interest_rate = Decimal(str(interest_rate))
        return interest_rate if interest_rate > 0 else Decimal("9.5")

    async def _evaluate_decision(
        self,
        state: LoanState,
        salary_amount: str | None = None,
    ) -> dict:
        return await evaluate_underwriting_decision_tool.ainvoke({
            "customer_id": str(state.get("customer_id")),
            "conversation_id": str(state.get("conversation_id")),
            "loan_amount": str(state.get("loan_amount")),
            "pre_approved_limit": str(state.get("pre_approved_limit")),
            "tenure_months": state.get("tenure_months"),
            "credit_score": state.get("credit_score") or 0,
            "salary_amount": salary_amount,
            "interest_rate": str(self._get_interest_rate(state)),
        })

    async def underwriting_node(self, state: LoanState) -> dict:
        required_fields = [
            "customer_id",
            "conversation_id",
            "loan_amount",
            "pre_approved_limit",
            "tenure_months",
            "credit_score",
        ]
        missing_fields = [
            field_name
            for field_name in required_fields
            if state.get(field_name) in (None, "", 0, Decimal("0"))
        ]
        if missing_fields:
            return {
                "next_agent": "underwriting",
                "messages": [
                    AIMessage(
                        content=(
                            "I need the complete loan and customer details before "
                            f"underwriting. Missing: {', '.join(missing_fields)}."
                        )
                    )
                ],
            }

        loan_amount = Decimal(str(state.get("loan_amount")))
        pre_approved_limit = Decimal(str(state.get("pre_approved_limit")))
        credit_score = state.get("credit_score") or 0

        if credit_score < MIN_CREDIT_SCORE or loan_amount <= pre_approved_limit:
            decision = await self._evaluate_decision(state)
            status = decision.get("status")
            rejection_reason = decision.get("rejection_reason")
            approved = status == "approved"
            return {
                "application_id": str(decision.get("application_id")),
                "interest_rate": self._get_interest_rate(state),
                "monthly_emi": Decimal(str(decision.get("monthly_emi"))),
                "credit_check_done": True,
                "under_writing_approved": approved,
                "final_status": status,
                "rejection_reason": rejection_reason,
                "next_agent": "sanction" if approved else "end",
                "messages": [
                    AIMessage(
                        content=(
                            "Underwriting complete.\n\n"
                            f"Status: {status}\n"
                            f"Monthly EMI: ₹{Decimal(str(decision.get('monthly_emi'))):,.2f}"
                            + (
                                f"\nReason: {rejection_reason}"
                                if rejection_reason
                                else ""
                            )
                        )
                    )
                ],
            }

        if loan_amount > Decimal("2") * pre_approved_limit:
            decision = await self._evaluate_decision(state)
            return {
                "application_id": str(decision.get("application_id")),
                "interest_rate": self._get_interest_rate(state),
                "monthly_emi": Decimal(str(decision.get("monthly_emi"))),
                "credit_check_done": True,
                "under_writing_approved": False,
                "final_status": "rejected",
                "rejection_reason": decision.get("rejection_reason"),
                "next_agent": "end",
                "messages": [
                    AIMessage(
                        content=(
                            "Underwriting complete.\n\n"
                            "Status: rejected\n"
                            f"Reason: {decision.get('rejection_reason')}"
                        )
                    )
                ],
            }

        if not state.get("salary_slip_uploaded"):
            pending_decision = await self._evaluate_decision(state)
            return {
                "monthly_emi": Decimal(str(pending_decision.get("monthly_emi"))),
                "credit_check_done": True,
                "next_agent": "underwriting",
                "messages": [
                    AIMessage(
                        content=(
                            "Your requested loan amount is above your "
                            "pre-approved limit, so I need your latest salary "
                            "slip to continue.\n\n"
                            f"Expected EMI: ₹{Decimal(str(pending_decision.get('monthly_emi'))):,.2f}\n"
                            "Please upload your salary slip from the last 6 months."
                        )
                    )
                ],
            }

        salary_slip_path = state.get("salary_slip_path")
        customer_id = state.get("customer_id")
        if not salary_slip_path or not customer_id:
            return {
                "next_agent": "underwriting",
                "messages": [
                    AIMessage(
                        content=(
                            "I need your verified customer profile and uploaded "
                            "salary slip before I can continue underwriting."
                        )
                    )
                ],
            }

        tool_result = await process_salary_slip_tool.ainvoke({
            "customer_id": str(customer_id),
            "salary_slip_path": salary_slip_path,
        })

        if not tool_result.get("success"):
            return {
                "next_agent": "underwriting",
                "messages": [
                    AIMessage(
                        content=(
                            tool_result.get("error")
                            or "I could not process the uploaded salary slip. Please upload a clearer file."
                        )
                    )
                ],
            }

        salary_slip_date = tool_result.get("salary_slip_date")
        salary_amount = tool_result.get("salary_amount")
        is_recent = tool_result.get("salary_slip_is_recent")

        updates = {
            "salary_slip_date": salary_slip_date,
            "salary_amount": float(salary_amount) if salary_amount else None,
        }

        if not is_recent:
            return {
                **updates,
                "next_agent": "underwriting",
                "messages": [
                    AIMessage(
                        content=(
                            "The uploaded salary slip appears to be older than "
                            "6 months. Please upload a salary slip from the last "
                            "6 months."
                        )
                    )
                ],
            }

        if not salary_amount:
            return {
                **updates,
                "next_agent": "underwriting",
                "messages": [
                    AIMessage(
                        content=(
                            "I processed the salary slip, but couldn't identify "
                            "the monthly salary. Please upload a clearer salary slip."
                        )
                    )
                ],
            }

        decision = await self._evaluate_decision(state, salary_amount=salary_amount)
        status = decision.get("status")
        rejection_reason = decision.get("rejection_reason")
        approved = status == "approved"

        return {
            **updates,
            "application_id": str(decision.get("application_id")),
            "interest_rate": self._get_interest_rate(state),
            "monthly_emi": Decimal(str(decision.get("monthly_emi"))),
            "credit_check_done": True,
            "under_writing_approved": approved,
            "final_status": status,
            "rejection_reason": rejection_reason,
            "next_agent": "sanction" if approved else "end",
            "messages": [
                AIMessage(
                    content=(
                        "Underwriting complete.\n\n"
                        f"Status: {status}\n"
                        f"Salary slip date: {salary_slip_date}\n"
                        f"Monthly salary: ₹{Decimal(str(salary_amount)):,.2f}\n"
                        f"Expected EMI: ₹{Decimal(str(decision.get('monthly_emi'))):,.2f}"
                        + (
                            f"\nReason: {rejection_reason}"
                            if rejection_reason
                            else ""
                        )
                    )
                )
            ],
        }
