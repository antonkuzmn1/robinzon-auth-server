from sqlalchemy.orm import Session

from app.logger import logger
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_companies(self):
        return self.db.query(Company).all()

    def get_company_by_id(self, company_id: int):
        return self.db.query(Company).filter(Company.id == company_id).first()

    def create_company(self, company_data: CompanyCreate):
        new_company = Company(**company_data.model_dump())
        self.db.add(company_data)
        self.db.commit()
        self.db.refresh(company_data)

        logger.info(f"Created new company: {new_company.id} - {new_company.name}")
        return company_data

    def update_company(self, company_id, company_data: CompanyUpdate):
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
        return company

    def delete_company(self, company_id: int):
        company = self.get_company_by_id(company_id)
        if not company:
            logger.warning(f"Attempt to delete non-existent company: {company_id}")
            return None

        setattr(company, "deleted", True)

        self.db.commit()
        self.db.refresh(company)

        logger.info(f"Company marked as deleted: {company.id} - {company.name}")
        return company
