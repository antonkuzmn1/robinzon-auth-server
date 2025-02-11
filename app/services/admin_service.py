from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.logger import logger
from app.models import Admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut
from app.services.auth_service import AuthService
from app.services.base_service import BaseService
from app.services.company_service import CompanyService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_service = AuthService()

class AdminService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Admin, AdminOut)

    def create(self, admin_data: AdminCreate) -> Optional[AdminOut]:
        hashed_password = pwd_context.hash(admin_data.password)
        new_admin = Admin(**admin_data.model_dump(exclude={"password"}), hashed_password=hashed_password)
        self.db.add(new_admin)
        self.db.commit()
        self.db.refresh(new_admin)

        logger.info(f"Created new admin: {new_admin.id} - {new_admin.username}")
        return AdminOut.model_validate(new_admin, from_attributes=True)

    def update(self, admin_id: int, admin_data: AdminUpdate) -> Optional[AdminOut]:
        admin = self.get_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to update non-existent admin: {admin_id}")
            return None

        update_data = admin_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])

        update_data.pop('password', None)

        for key, value in update_data.items():
            setattr(admin, key, value)

        self.db.commit()
        self.db.refresh(admin)

        logger.info(f"Updated admin: {admin.id} - {admin.username}")

        admin_out = AdminOut.model_validate(admin, from_attributes=True)

        return admin_out

    def create_m2m_admin_company(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = self.get_by_id(admin_id)
        company = CompanyService(self.db).get_by_id(company_id)

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
        admin = self.get_by_id(admin_id)
        company = CompanyService(self.db).get_by_id(company_id)

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

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_admin(self, username: str, password: str):
        admin = self.get_by_username(username)
        if not admin or not self.verify_password(password, admin.hashed_password):
            return None
        return admin

    @classmethod
    def create_admin_token(cls, admin) -> str:
        token_data = {"sub": admin.username, "role": "admin"}
        return auth_service.create_access_token(token_data)