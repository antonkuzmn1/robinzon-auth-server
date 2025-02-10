from datetime import datetime, UTC
from typing import List, Optional, Type, TypeVar, cast
from sqlalchemy.orm import Session
from app.logger import logger

T = TypeVar("T")
SchemaOut = TypeVar("SchemaOut")
SchemaBase = TypeVar("SchemaBase")


class BaseService:
    def __init__(self, db: Session, model: Type[T], schema_out: Type[SchemaOut]):
        self.db = db
        self.model = model
        self.schema_out = schema_out

    def get_all(self) -> List[SchemaOut]:
        records = self.db.query(self.model).all()

        def _to_dict(obj):
            return {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}

        return [
            self.schema_out.model_validate(
                {**_to_dict(record), "updated_at": record.updated_at or datetime.now()}
            )
            for record in records
        ]

    def get_by_id(self, record_id: int) -> Optional[SchemaOut]:
        record = self.db.query(self.model).filter(cast("ColumnElement[bool]", self.model.id == record_id)).first()
        if record:
            record_dict = {key: value for key, value in record.__dict__.items() if not key.startswith('_')}

            record_dict.setdefault('created_at', datetime.now(UTC))
            record_dict.setdefault('updated_at', datetime.now(UTC))

            return self.schema_out.model_validate(record_dict)
        return None

    def create(self, data: SchemaBase) -> Optional[SchemaOut]:
        new_record = self.model(**data.model_dump())
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)

        logger.info(f"Created new {self.model.__name__}: {new_record.id}")
        return self.schema_out.model_validate(new_record, from_attributes=True)

    def update(self, record_id: int, data: SchemaBase) -> Optional[SchemaOut]:
        record = self.db.query(self.model).filter(cast("ColumnElement[bool]", self.model.id == record_id)).first()
        if not record:
            logger.warning(f"Attempt to update non-existent {self.model.__name__}: {record_id}")
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        self.db.commit()
        self.db.refresh(record)

        logger.info(f"Updated {self.model.__name__}: {record.id}")
        return self.schema_out.model_validate(record, from_attributes=True)

    def delete(self, record_id: int) -> Optional[SchemaOut]:
        record = self.db.query(self.model).filter(cast("ColumnElement[bool]", self.model.id == record_id)).first()
        if not record:
            logger.warning(f"Attempt to delete non-existent {self.model.__name__}: {record_id}")
            return None

        setattr(record, "deleted", True)
        self.db.commit()
        self.db.refresh(record)

        logger.info(f"{self.model.__name__} marked as deleted: {record.id}")
        return self.schema_out.model_validate(record, from_attributes=True)
