from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator

from app.core.constants import (
    DESCRIPTION_MAX_LEN,
    DESCRIPTION_MIN_LEN,
    FULL_AMOUNT_GT,
    INVESTED_AMOUNT_DEFAULT,
    PROJECTNAME_MAX_LEN,
    PROJECTNAME_MIN_LEN
)


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=PROJECTNAME_MIN_LEN,
        max_length=PROJECTNAME_MAX_LEN
    )
    description: Optional[str] = Field(
        None,
        min_length=DESCRIPTION_MIN_LEN,
        max_length=DESCRIPTION_MAX_LEN
    )
    full_amount: Optional[int] = Field(None, gt=FULL_AMOUNT_GT)

    @root_validator(pre=True)
    def check_forbidden_fields(cls, values):
        forbidden_fields = {
            "invested_amount", "create_date", "close_date", "fully_invested"
        }
        for field in forbidden_fields:
            if field in values:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f'Нельзя изменять поле {field}',
                )
        return values


class CharityProjectCreate(BaseModel):
    name: str = Field(
        min_length=PROJECTNAME_MIN_LEN,
        max_length=PROJECTNAME_MAX_LEN
    )
    description: str = Field(min_length=DESCRIPTION_MIN_LEN)
    full_amount: int = Field(..., gt=FULL_AMOUNT_GT)
    invested_amount: int = INVESTED_AMOUNT_DEFAULT
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
