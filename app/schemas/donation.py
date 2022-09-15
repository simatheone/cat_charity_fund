from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime = Field(datetime.now())
    close_date: datetime

    class Config:
        orm_mode = True
