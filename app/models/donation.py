from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, Boolean
from sqlalchemy.sql import func

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id', name='fk_reservation_user_id_user'))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, server_default=func.now())
    close_date = Column(DateTime)