from typing import List, Optional

from sqlalchemy.orm import Session

from app.logger import logger
from app.models.user import User
from app.schemas.user import UserOut, UserBase


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[UserOut]:
        users = self.db.query(User).all()
        return [UserOut.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        user = self.db.query(User).filter(User.id == user_id).first()
        return UserOut.model_validate(user) if user else None

    def create_user(self, user_data: UserBase) -> Optional[UserOut]:
        user = User(**user_data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(f"Created new user: {user.id} - {user.username}")
        return UserOut.model_validate(user, from_attributes=True)

    def update_user(self, user_id, user_data: UserBase) -> Optional[UserOut]:
        user = self.get_user_by_id(user_id)
        if not user:
            logger.warning(f"Attempt to update non-existent user: {user_id}")
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        logger.info(f"Updated user: {user.id} - {user.username}")
        return UserOut.model_validate(user, from_attributes=True)

    def delete_user(self, user_id) -> Optional[UserOut]:
        user = self.get_user_by_id(user_id)
        if not user:
            logger.warning(f"Attempt to delete non-existent user: {user_id}")
            return None

        setattr(user, "deleted", True)

        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User marked as deleted: {user.id} - {user.username}")
        return UserOut.model_validate(user, from_attributes=True)