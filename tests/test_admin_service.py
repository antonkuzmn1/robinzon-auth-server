import pytest
from unittest.mock import MagicMock
from app.services.admin_service import AdminService
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def service(db):
    return AdminService(db)


def test_create(service, db):
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None

    admin_data = AdminCreate(
        username="admin",
        password="securepassword",
        surname="surname",
        name="name",
    )

    new_admin = service.create(admin_data)

    assert new_admin.password != "securepassword"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_update(service, db):
    admin = Admin(
        id=1,
        username="admin",
        password="securepassword",
        surname="surname",
        name="name",
    )

    db.query.return_value.filter.return_value.first.return_value = admin

    update_data = AdminUpdate(
        username="admin",
        password="securepassword",
        surname="new_surname",
        name="name",
    )
    updated_admin = service.update(1, update_data)

    assert updated_admin.surname == "new_surname"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_delete(service, db):
    admin = Admin(
        id=1,
        username="admin",
        password="securepassword",
        surname="surname",
        name="name",
    )

    db.query.return_value.filter.return_value.first.return_value = admin

    deleted_admin = service.delete(1)

    assert deleted_admin.deleted is True
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
