from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.company import CompanyOut, CompanyCreate, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=List[CompanyOut])
def get_all_companies(db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.get_all_companies()


@router.get("/{company_id}", response_model=CompanyOut)
def get_company_by_id(company_id: int, db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.get_company_by_id(company_id)


@router.post("/", response_model=CompanyOut)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.create_company(company)


@router.put("/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.update_company(company_id, company)


@router.delete("/{company_id}", response_model=CompanyOut)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.delete_company(company_id)
