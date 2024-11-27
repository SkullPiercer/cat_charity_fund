from cgitb import reset

from requests import session
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

            need_to_close = project.full_amount - project.invested_amount
            founds = donation.full_amount - donation.invested_amount

            if founds > need_to_close:
                project.invested_amount = project.full_amount
                project.fully_invested = True
                project.close_date = datetime.now()
                donation.invested_amount += need_to_close

            elif founds == need_to_close:
                project.invested_amount = project.full_amount
                donation.invested_amount = donation.full_amount
                donation.fully_invested = True
                project.fully_invested = True
                project.close_date = datetime.now()
                donation.close_date = datetime.now()
            else:
                donation.fully_invested = True
                donation.invested_amount = donation.full_amount
                donation.close_date = datetime.now()
                project.invested_amount += founds

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True

    session.add_all(donations)
    session.add_all(projects)
    await session.commit()


async def project_invest(
        project: CharityProject,
        session: AsyncSession
):
    donations = await session.execute(
        select(Donation).where(Donation.fully_invested == False).order_by(Donation.create_date)
    )

    for donation in donations.scalars().all():
        if project.fully_invested:
            break

        founds = donation.full_amount - donation.invested_amount
        need_to_close = project.full_amount - project.invested_amount

        if founds > need_to_close:
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += need_to_close
        elif founds == need_to_close:
            project.invested_amount = project.full_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.close_date = datetime.now()
        else:
            donation.fully_invested = True
            donation.invested_amount = donation.full_amount
            donation.close_date = datetime.now()
            project.invested_amount += founds

    session.add(project)
    session.add_all(donations)
    await session.commit()
    return project

async def donation_invest(
        donation: Donation,
        session: AsyncSession
):
    projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == False).order_by(CharityProject.create_date)
    )
    for project in projects.scalars().all():
        if donation.fully_invested:
            break

        need_to_close = project.full_amount - project.invested_amount
        founds = donation.full_amount - donation.invested_amount

        if founds > need_to_close:
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += need_to_close

        elif founds == need_to_close:
            project.invested_amount = project.full_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.close_date = datetime.now()
        else:
            donation.fully_invested = True
            donation.invested_amount = donation.full_amount
            donation.close_date = datetime.now()
            project.invested_amount += founds

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True

    session.add(donation)
    session.add_all(projects)
    await session.commit()
    return donation