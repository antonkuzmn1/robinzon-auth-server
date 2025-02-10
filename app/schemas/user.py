from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.company import CompanyOut


class UserBase(BaseModel):
    username: str
    surname: str
    name: str
    middlename: Optional[str] = None
    department: Optional[str] = None
    remote_workplace: Optional[str] = None
    local_workplace: Optional[str] = None
    phone: Optional[str] = None
    cellular: Optional[str] = None
    post: Optional[str] = None
    company_id: int
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    company: CompanyOut
