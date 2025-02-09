from typing import List, Optional

from sqlalchemy.orm import Session

from app.logger import logger
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut
from passlib.context import CryptContext

from app.services.company_service import CompanyService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_admins(self) -> List[AdminOut]:
        admins = self.db.query(Admin).all()
        return [AdminOut.model_validate(admin) for admin in admins]

    def get_admin_by_id(self, admin_id: int) -> Optional[AdminOut]:
        admin = self.db.query(Admin).filter(Admin.id == admin_id).first()
        return AdminOut.model_validate(admin) if admin else None

    def create_admin(self, admin_data: AdminCreate) -> Optional[AdminOut]:
        hashed_password = pwd_context.hash(admin_data.password)
        new_admin = Admin(**admin_data.model_dump(exclude={"password"}), password=hashed_password)
        self.db.add(new_admin)
        self.db.commit()
        self.db.refresh(new_admin)

        logger.info(f"Created new admin: {new_admin.id} - {new_admin.username}")
        return AdminOut.model_validate(new_admin, from_attributes=True)

    def update_admin(self, admin_id: int, admin_data: AdminUpdate) -> Optional[AdminOut]:
        admin = self.get_admin_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to update non-existent admin: {admin_id}")
            return None

        update_data = admin_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])

        for key, value in update_data.items():
            setattr(admin, key, value)

        self.db.commit()
        self.db.refresh(admin)

        logger.info(f"Updated admin: {admin.id} - {admin.username}")
        return AdminOut.model_validate(admin, from_attributes=True)

    def delete_admin(self, admin_id: int) -> Optional[AdminOut]:
        admin = self.get_admin_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to delete non-existent admin: {admin_id}")
            return None

        setattr(admin, "deleted", True)

        self.db.commit()
        self.db.refresh(admin)

        logger.info(f"Admin marked as deleted: {admin.id} - {admin.username}")
        return AdminOut.model_validate(admin, from_attributes=True)

    def create_m2m_admin_company(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.get_admin_by_id(admin_id)
        company = CompanyService(self.db).get_company_by_id(company_id)

        # noinspection DuplicatedCode
        if admin and company:
            admin.companies.append(company)
            self.db.commit()
            self.db.refresh(company)
            logger.info(f"Admin {admin.username} related to company: {company.id} - {company.name}")
            return AdminOut.model_validate(admin, from_attributes=True)
        else:
            logger.warning("Admin or company not found")
            return None

    def remove_m2m_admin_company(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.get_admin_by_id(admin_id)
        company = CompanyService(self.db).get_company_by_id(company_id)

        # noinspection DuplicatedCode
        if admin and company:
            if company in admin.companies:
                admin.companies.remove(company)
                self.db.commit()
                self.db.refresh(company)
                logger.info(f"Admin {admin.username} removed from company: {company.id} - {company.name}")
                return AdminOut.model_validate(admin, from_attributes=True)
            else:
                logger.warning("Admin in company not found")
                return None
        else:
            logger.warning("Admin or company not found")
            return None
