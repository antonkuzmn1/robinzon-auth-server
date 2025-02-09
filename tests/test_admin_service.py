import pytest
from unittest.mock import MagicMock
from app.services.admin_service import AdminService
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def admin_service(mock_db):
    return AdminService(mock_db)

def test_create_admin(admin_service, mock_db):
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    admin_data = AdminCreate(
        username="admin",
        password="securepassword",
        surname="surname",
        name="name",
    )

    new_admin = admin_service.create_admin(admin_data)

    assert new_admin.password != "securepassword"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_admin(admin_service, mock_db):
    admin = Admin(
        id=1,
        username="admin",
        password="securepassword",
        surname="surname",
        name="name",
    )
    mock_db.query.return_value.filter.return_value.first.return_value = admin

    update_data = AdminUpdate(surname="new_surname")
    updated_admin = admin_service.update_admin(1, update_data)

    assert updated_admin.surname == "new_surname"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_admin(admin_service, mock_db):
    admin = Admin(
        id=1,
        username="admin",
        password="securepassword",
        surname="surname",
        name="name",
    )

    mock_db.query.return_value.filter.return_value.first.return_value = admin

    deleted_admin = admin_service.delete_admin(1)

    assert deleted_admin.deleted is True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()