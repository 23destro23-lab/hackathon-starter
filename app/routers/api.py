from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import example as crud
from app.schemas.example import ExampleItemCreate, ExampleItemRead, ExampleItemUpdate

router = APIRouter(tags=["example items"])


@router.get("/items", response_model=list[ExampleItemRead])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@router.post("/items", response_model=ExampleItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ExampleItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, payload)


@router.get("/items/{item_id}", response_model=ExampleItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/items/{item_id}", response_model=ExampleItemRead)
def update_item(item_id: int, payload: ExampleItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db, item, payload)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return None
