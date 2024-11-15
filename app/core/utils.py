from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation, CharityProject
from datetime import datetime
from sqlalchemy import select
from app.core.db import get_async_session
from fastapi.params import Depends


async def invest_funds(
        session: AsyncSession = Depends(get_async_session)
) -> None:
    projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == False).order_by(CharityProject.create_date)
    )
    donations = await session.execute(
        select(Donation).where(Donation.fully_invested == False).order_by(Donation.create_date)
    )

    projects = projects.scalars().all()
    donations = donations.scalars().all()

    for donation in donations:
        for project in projects:
            if donation.fully_invested:
                break

            amount_to_invest = min(
                project.full_amount - project.invested_amount,
                donation.full_amount - donation.invested_amount
            )

            project.invested_amount += amount_to_invest
            donation.invested_amount += amount_to_invest

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()

    await session.commit()
