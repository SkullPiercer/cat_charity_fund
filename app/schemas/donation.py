from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field



class DonationCreate(BaseModel):
    # user_id: int
    comment: Optional[str] = None
    full_amount: int = Field(..., gt=0)
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = Field(default_factory=datetime.now)
    close_date: datetime = None

class DonationDB(DonationCreate):
    id: int

    class Config:
        orm_mode = True

class DonationUserSchema(BaseModel):
    id: int
    comment: Optional[str]
    full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdminSchema(DonationUserSchema):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]