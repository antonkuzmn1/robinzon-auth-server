from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyOut
from app.services.base_service import BaseService


class CompanyService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Company, CompanyOut)