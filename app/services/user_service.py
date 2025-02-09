from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserOut
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, User, UserOut)
