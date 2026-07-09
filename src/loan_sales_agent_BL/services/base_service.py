from math import ceil
from typing import List

from src.loan_sales_agent_shared.models.pagination_model import PaginatedResponse, T, PaginatedMeta

def paginated_response(
        records: List[T],
        total: int,
        page: int,
        per_page: int
) -> PaginatedResponse[T]:
    return PaginatedResponse(
        records=records,
        meta = PaginatedMeta(
            total=total,
            page=page,
            per_page=per_page,
            total_pages=ceil(total / per_page) if total else 0,
        ),
    )