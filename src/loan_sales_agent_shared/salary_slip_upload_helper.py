from pathlib import Path
from fastapi import UploadFile

from src.loan_sales_agent_shared.config import SALARY_SLIP_DIR

async def save_salary_slip(
        customer_id,
        file: UploadFile
) -> str:

    SALARY_SLIP_DIR.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename).suffix

    filepath = SALARY_SLIP_DIR / f"{customer_id}{extension}"

    with open(filepath, "wb") as f:
        f.write(await file.read())

    return str(filepath)