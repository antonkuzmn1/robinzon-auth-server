from sqlalchemy.orm import Session

from app.logger import logger
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_admins(self):
        return self.db.query(Admin).all()

    def get_admin_by_id(self, admin_id: int):
        return self.db.query(Admin).filter(Admin.id == admin_id).first()

    def create_admin(self, admin_data: AdminCreate):
        hashed_password = pwd_context.hash(admin_data.password)
        new_admin = Admin(**admin_data.model_dump(exclude={"password"}), password=hashed_password)
        self.db.add(new_admin)
        self.db.commit()
        self.db.refresh(new_admin)

        logger.info(f"Created new admin: {new_admin.id} - {new_admin.username}")
        return new_admin

    def update_admin(self, admin_id: int, admin_data: AdminUpdate):
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
        return admin

    def delete_admin(self, admin_id: int):
        admin = self.get_admin_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to delete non-existent admin: {admin_id}")
            return None

        setattr(admin, "deleted", True)

        self.db.commit()
        self.db.refresh(admin)

        logger.info(f"Admin marked as deleted: {admin.id} - {admin.username}")
        return admin
