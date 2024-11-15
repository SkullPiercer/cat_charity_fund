from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.schemas.donation import DonationDB, DonationCreate
from app.crud.donation import donation_crud
from app.core.user import current_user
from app.core.utils import invest_funds

router = APIRouter()

@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(invest_funds), Depends(current_user)]
)
async def create_new_project(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(donation, session)
    return new_donation

@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    if user.role != 'admin':
        all_projects = await donation_crud.get_by_user(
            session=session, user=user
        )
    else:
        all_projects = await donation_crud.get_multi(session)
    return all_projects