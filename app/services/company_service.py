from typing import List, Optional

from sqlalchemy.orm import Session

from app.logger import logger
from app.models.company import Company
from app.schemas.company import CompanyOut, CompanyBase


class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_companies(self) -> List[CompanyOut]:
        companies = self.db.query(Company).all()
        return [CompanyOut.model_validate(company) for company in companies]

    def get_company_by_id(self, company_id: int) -> Optional[CompanyOut]:
        company = self.db.query(Company).filter(Company.id == company_id).first()
        return CompanyOut.model_validate(company) if company else None

    def create_company(self, company_data: CompanyBase) -> Optional[CompanyOut]:
        new_company = Company(**company_data.model_dump())
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)

        logger.info(f"Created new company: {new_company.id} - {new_company.name}")
        return CompanyOut.model_validate(new_company, from_attributes=True)

    def update_company(self, company_id, company_data: CompanyBase) -> Optional[CompanyOut]:
        company = self.get_company_by_id(company_id)
        if not company:
            logger.warning(f"Attempt to update non-existent company: {company_id}")
            return None

        update_data = company_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(company, key, value)

        self.db.commit()
        self.db.refresh(company)

        logger.info(f"Updated company: {company.id} - {company.name}")
        return CompanyOut.model_validate(company, from_attributes=True)

    def delete_company(self, company_id: int) -> Optional[CompanyOut]:
        company = self.get_company_by_id(company_id)
        if not company:
            logger.warning(f"Attempt to delete non-existent company: {company_id}")
            return None

        setattr(company, "deleted", True)

        self.db.commit()
        self.db.refresh(company)

        logger.info(f"Company marked as deleted: {company.id} - {company.name}")
        return CompanyOut.model_validate(company, from_attributes=True)
