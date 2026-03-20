from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from langchain.tools import tool

from ..workflow.state import LoanState
from config import SANCTION_LETTER_PATH

@tool
def generate_sanction_letter_pdf(state: LoanState) -> str:
    """
    This function is used for generating sanction letters
    """
    filename = f"{state['application_id']}.pdf"
    filepath = SANCTION_LETTER_PATH / filename
    
    c = canvas.Canvas(str(filepath), pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "XYZ finance ltd.")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    c.drawString(50, height - 95, f"Ref No: SL/{state['application_id']}")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 130, "To,")
    c.setFont("Helvetica", 11)

    c.drawString(50, height - 145, f"{state.get('customer_name', 'N/A')}")
    c.drawString(50, height - 160, f"{state.get('customer_address', '[Borrower Address]')}")
    c.drawString(50, height - 175, f"Contact: {state.get('customer_phone', '[Contact Number]')}")

    c.setFont("Helvetica-Bold", 11)
    subject = "Subject: Sanction of Personal/Business Loan Facility"
    c.drawString(50, height - 210, subject)

    subj_width = c.stringWidth(subject, "Helvetica-Bold", 11)
    c.line(50, height - 212, 50 + subj_width, height - 212)
    
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 240, f"Dear {state['customer_name']},")
    
    opening_text = [
        f"With reference to your application dated {state.get('application_date', 'N/A')}, we are pleased to inform",
        "you that your loan request has been technically and administratively processed. We have",
        "sanctioned a loan facility under the following terms and conditions:"
    ]
    
    y_position = height - 265
    for line in opening_text:
        c.drawString(50, y_position, line)
        y_position -= 15
        
    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Loan Terms:")
    c.setFont("Helvetica", 11)
    
    y_position -= 25
    terms = [
        f"Application ID: {state['application_id']}",
        f"Sanctioned Amount: ₹{state['loan_amount']:,.2f}",
        f"Interest Rate: {state['interest_rate']}% per annum",
        f"Tenure: {state['tenure_months']} months",
        f"Monthly EMI: ₹{state['monthly_emi']:,.2f}",
    ]
    
    for term in terms:
        c.drawString(70, y_position, f"• {term}")
        y_position -= 20
        
    y_position -= 10
    c.drawString(50, y_position, "The loan amount will be disbursed to your registered bank account within 24-48 hours.")
    
    c.setFont("Helvetica-Italic", 9)
    c.drawCentredString(width / 2, 50, "This is a computer-generated document and does not require a physical signature.")
    
    c.save()
    return str(filepath)