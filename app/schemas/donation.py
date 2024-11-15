from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field, validator


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: int = Field(..., gt=0)
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now()
    close_date: datetime = None

class DonationDB(DonationCreate):
    id: int

    class Config:
        orm_mode = True