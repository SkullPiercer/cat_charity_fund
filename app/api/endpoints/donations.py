from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.schemas.donation import DonationDB, DonationCreate, DonationUserSchema
from app.crud.donation import donation_crud
from app.crud.projects import projects_crud
from app.core.user import current_user, current_superuser
from app.core.utils import invest_funds, donation_invest

router = APIRouter()

@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    available_projects = await projects_crud.get_not_full_invested(session)
    donation_invest(donation=new_donation, projects=available_projects)
    await session.commit()
    await session.refresh(new_donation)
    return DonationUserSchema.from_orm(new_donation)

@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    dependencies=[Depends(invest_funds)]
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    all_projects = await donation_crud.get_by_user(
        session=session, user=user
    )
    all_projects = [DonationUserSchema.from_orm(donation) for donation in all_projects]
    return all_projects


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser), Depends(invest_funds)],

)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await donation_crud.get_multi(session)
    return all_projects

