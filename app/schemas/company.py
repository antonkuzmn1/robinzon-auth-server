from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing_extensions import Optional

from app.schemas.admin import AdminOut


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompanyOut(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    admins: list[AdminOut] = []

    model_config = ConfigDict(from_attributes=True)
