from datetime import datetime

from pydantic import BaseModel, Field, validator


class CharityProjectUpdate(BaseModel):
    name: str
    description: str
    full_amount: int = Field(..., gt=0)

    # @validator('full_amount')
    # def validate_amount(self):

class CharityProjectCreate(BaseModel):
    name: str
    description: str
    full_amount: int = Field(..., gt=0)
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now()
    close_date: datetime = None

class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True