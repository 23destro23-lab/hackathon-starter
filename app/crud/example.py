from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.example import ExampleItem
from app.schemas.example import ExampleItemCreate, ExampleItemUpdate


def get_items(db: Session) -> list[ExampleItem]:
    return list(db.scalars(select(ExampleItem).order_by(ExampleItem.created_at.desc())))


def get_item(db: Session, item_id: int) -> ExampleItem | None:
    return db.get(ExampleItem, item_id)


def create_item(db: Session, data: ExampleItemCreate) -> ExampleItem:
    item = ExampleItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item: ExampleItem, data: ExampleItemUpdate) -> ExampleItem:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: ExampleItem) -> None:
    db.delete(item)
    db.commit()
