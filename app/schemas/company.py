from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .admin import AdminOut

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompanyOut(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    admins: list["AdminOut"] = []

    class Config:
        from_attributes = True

CompanyOut.update_forward_refs()