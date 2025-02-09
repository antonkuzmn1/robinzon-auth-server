from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    username: Optional[str] = None
    surname: Optional[str] = None
    name: Optional[str] = None


class AdminOut(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime
