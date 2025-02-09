from fastapi import APIRouter, Depends
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Session
from app.services.admin_service import AdminService
from app.db import get_db, Base
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from typing import List

router = APIRouter(prefix="/admins", tags=["Admins"])

admin_company_association = Table(
    "admin_company_association",
    Base.metadata,
    Column("admin_id", Integer, ForeignKey("admins.id"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
)

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


@router.post("/{admin_id}/companies/{company_id}", response_model=AdminOut)
def create_m2m_admin_company(admin_id: int, company_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.create_m2m_admin_company(admin_id, company_id)


@router.delete("/{admin_id}/companies/{company_id}", response_model=AdminOut)
def remove_m2m_admin_company(admin_id: int, company_id: int, db: Session = Depends(get_db)):
    service = AdminService(db)
    return service.remove_m2m_admin_company(admin_id, company_id)