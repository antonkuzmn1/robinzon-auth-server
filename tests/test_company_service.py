from unittest.mock import MagicMock

import pytest

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.company_service import CompanyService


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def company_service(mock_db):
    return CompanyService(mock_db)


def test_create_company(company_service, mock_db):
    mock_db.add.return_value = True
    mock_db.commit.return_value = True
    mock_db.refresh.return_value = True

    company_data = CompanyCreate(
        name="company",
    )

    new_company = company_service.create_company(company_data)

    assert new_company.name == "company"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_update_company(company_service, mock_db):
    company = Company(
        name="company",
    )

    mock_db.query.return_value.filter.return_value.all.return_value = company

    update_company = CompanyUpdate(name="updated company")
    updated_company = company_service.update_company(1, update_company)

    assert updated_company.name == "updated company"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_delete_company(company_service, mock_db):
    company = Company(
        name="company",
    )

    mock_db.query.return_value.filter.return_value.all.return_value = company

    deleted_company = company_service.delete_company(1)

    assert deleted_company.deleted is True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
