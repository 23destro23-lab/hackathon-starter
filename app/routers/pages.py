from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import example as crud
from app.schemas.example import ExampleItemCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"items": crud.get_items(db)},
    )


@router.post("/items")
def add_item(
    title: str = Form(..., min_length=1, max_length=200),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    crud.create_item(db, ExampleItemCreate(title=title.strip(), description=description.strip() or None))
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/items/{item_id}/delete")
def remove_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is not None:
        crud.delete_item(db, item)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
