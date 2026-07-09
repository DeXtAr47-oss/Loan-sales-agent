from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedMeta(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    records: List[T]
    meta: PaginatedMeta
