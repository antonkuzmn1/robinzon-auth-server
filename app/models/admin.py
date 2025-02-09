from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.db import Base
from app.models.admin_company_association import admin_company_association


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    middlename = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    cellular = Column(String(20), nullable=True)
    post = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    companies = relationship("Company", secondary=admin_company_association, back_populates="admins")
