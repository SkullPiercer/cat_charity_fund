from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonations(CRUDBase):
    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return user_donations.scalars().all()


donation_crud = CRUDDonations(Donation)
