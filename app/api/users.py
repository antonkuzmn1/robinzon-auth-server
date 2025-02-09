from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.user import UserOut, UserBase
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)


@router.post("/", response_model=UserOut)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update_user(user_id, user)


@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)
