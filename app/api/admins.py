from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.admin_service import AdminService
from app.db import get_db
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from typing import List

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.get("/", response_model=List[AdminOut])
def get_all_admins(db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.get_all_admins()

@router.get("/{admin_id}", response_model=AdminOut)
def get_admin_by_id(admin_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.get_admin_by_id(admin_id)

@router.post("/", response_model=AdminOut)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.create_admin(admin)

@router.put("/{admin_id}", response_model=AdminOut)
def update_admin(admin_id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.update_admin(admin_id, admin)

@router.delete("/{admin_id}", response_model=AdminOut)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.delete_admin(admin_id)