from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompanyOut(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
