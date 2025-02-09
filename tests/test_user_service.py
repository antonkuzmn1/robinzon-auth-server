from unittest.mock import MagicMock

import pytest

from app.models.user import User
from app.schemas.user import UserBase
from app.services.user_service import UserService


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def service(db):
    return UserService(db)


def test_create(service, db):
    db.add.return_value = True
    db.commit.return_value = True
    db.refresh.return_value = True

    data = UserBase(
        username="user",
        password="securepassword",
        surname="surname",
        name="name",
        company_id=1,
    )

    entity = service.create(data)

    assert entity.password == "securepassword"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_update(service, db):
    data = User(
        id=1,
        username="user",
        password="securepassword",
        surname="surname",
        name="name",
        company_id=1,
    )

    db.query.return_value.filter.return_value.first.return_value = data

    updated_data = UserBase(
        username="user",
        password="securepassword",
        surname="new_surname",
        name="name",
        company_id=1,
    )
    updated_entity = service.update(1, updated_data)

    assert updated_entity.surname == "new_surname"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_delete(service, db):
    data = User(
        id=1,
        username="user",
        password="securepassword",
        surname="surname",
        name="name",
        company_id=1,
    )

    db.query.return_value.filter.return_value.first.return_value = data

    deleted_entity = service.delete(1)

    assert deleted_entity.deleted is True
    db.query.assert_called_once()
    db.commit.assert_called_once()