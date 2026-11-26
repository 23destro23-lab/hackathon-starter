from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExampleItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class ExampleItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class ExampleItemRead(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
