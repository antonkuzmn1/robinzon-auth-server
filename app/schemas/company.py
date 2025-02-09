from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None


class CompanyOut(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
