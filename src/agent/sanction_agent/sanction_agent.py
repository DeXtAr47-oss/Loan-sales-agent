from datetime import datetime
from decimal import Decimal
from pathlib import Path

from langchain_community.tools import tool
from langchain_core.messages import AIMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.agent.states.state import LoanState
from src.loan_sales_agent_shared.config import SANCTION_LETTER_PATH


@tool
async def generate_sanction_letter_tool(
    application_id: str,
    customer_id: str,
    customer_name: str,
    customer_address: str,
    customer_phone: str,
    loan_amount: str,
    interest_rate: str,
    tenure_months: int,
    monthly_emi: str,
):
    """Generate a sanction letter PDF and store it in sanction_letters."""
    sanction_dir = Path(SANCTION_LETTER_PATH)
    sanction_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{customer_id}-sanctionletter-1.pdf"
    filepath = sanction_dir / filename

    pdf = canvas.Canvas(str(filepath), pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 50, "ABC Finance Ltd.")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 80, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    pdf.drawString(50, height - 95, f"Ref No: SL/{application_id}")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, height - 130, "To,")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, height - 145, customer_name or "N/A")
    pdf.drawString(50, height - 160, customer_address or "N/A")
    pdf.drawString(50, height - 175, f"Contact: {customer_phone or 'N/A'}")

    pdf.setFont("Helvetica-Bold", 11)
    subject = "Subject: Sanction of Loan Facility"
    pdf.drawString(50, height - 210, subject)
    subject_width = pdf.stringWidth(subject, "Helvetica-Bold", 11)
    pdf.line(50, height - 212, 50 + subject_width, height - 212)

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, height - 240, f"Dear {customer_name or 'Customer'},")

    opening_lines = [
        "We are pleased to inform you that your loan request has been processed",
        "and approved. The sanctioned loan facility is subject to the following",
        "terms and conditions:",
    ]

    y_position = height - 265
    for line in opening_lines:
        pdf.drawString(50, y_position, line)
        y_position -= 15

    y_position -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y_position, "Loan Terms:")
    pdf.setFont("Helvetica", 11)

    loan_amount_decimal = Decimal(str(loan_amount))
    monthly_emi_decimal = Decimal(str(monthly_emi))

    terms = [
        f"Application ID: {application_id}",
        f"Sanctioned Amount: Rs. {loan_amount_decimal:,.2f}",
        f"Interest Rate: {interest_rate}% per annum",
        f"Tenure: {tenure_months} months",
        f"Monthly EMI: Rs. {monthly_emi_decimal:,.2f}",
    ]

    y_position -= 25
    for term in terms:
        pdf.drawString(70, y_position, f"- {term}")
        y_position -= 20

    y_position -= 10
    pdf.drawString(
        50,
        y_position,
        "The loan amount will be disbursed to your registered bank account after final checks.",
    )

    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(
        width / 2,
        50,
        "This is a computer-generated document and does not require a physical signature.",
    )

    pdf.save()

    return {
        "sanction_letter_path": str(filepath),
        "sanction_letter_url": f"/api/sanction-letter/{filename}",
    }


class SanctionAgent:
    async def sanction_node(self, state: LoanState) -> dict:
        if (
            not state.get("application_id")
            or state.get("final_status") != "approved"
            or not state.get("under_writing_approved")
        ):
            return {
                "next_agent": "end",
                "messages": [
                    AIMessage(
                        content="A sanction letter can only be generated for an approved loan application."
                    )
                ],
            }

        customer_data = state.get("customer_data") or {}
        tool_result = await generate_sanction_letter_tool.ainvoke({
            "application_id": str(state.get("application_id")),
            "customer_id": str(state.get("customer_id")),
            "customer_name": state.get("customer_name") or customer_data.get("name") or "Customer",
            "customer_address": customer_data.get("address") or "",
            "customer_phone": customer_data.get("phone") or "",
            "loan_amount": str(state.get("loan_amount")),
            "interest_rate": str(state.get("interest_rate")),
            "tenure_months": state.get("tenure_months"),
            "monthly_emi": str(state.get("monthly_emi")),
        })

        return {
            **tool_result,
            "next_agent": "end",
            "messages": [
                AIMessage(
                    content=(
                        "Your loan has been approved and the sanction letter is ready. "
                        "You can download the PDF from the link below."
                    )
                )
            ],
        }
