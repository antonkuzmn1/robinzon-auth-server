from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .company import CompanyOut

class AdminBase(BaseModel):
    username: str
    surname: str
    name: str
    middlename: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    cellular: Optional[str] = None
    post: Optional[str] = None


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(AdminBase):
    password: Optional[str] = None


class AdminOut(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime
    companies: list["CompanyOut"] = []

    class Config:
        from_attributes = True

AdminOut.update_forward_refs()