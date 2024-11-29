from datetime import datetime
from fastapi import HTTPException
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    full_amount: Optional[int] = Field(None, gt=0)

    @root_validator(pre=True)
    def check_forbidden_fields(cls, values):
        forbidden_fields = {
            "invested_amount", "create_date", "close_date", "fully_invested"
        }
        for field in forbidden_fields:
            if field in values:
                raise HTTPException(
                    status_code=422,
                    detail=f'Нельзя изменять поле {field}',
                )
        return values


class CharityProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=101)
    description: str = Field(min_length=1)
    full_amount: int = Field(..., gt=0)
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = Field(default_factory=datetime.now)
    close_date: datetime = None

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    @validator('description')
    def desc_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
