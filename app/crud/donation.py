from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.models import User


class CRUDDonations(CRUDBase):
    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        user_reservations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return user_reservations.scalars().all()

donation_crud = CRUDDonations(Donation)