from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.schemas.donation import DonationDB, DonationCreate, DonationUserSchema, DonationAdminSchema
from app.crud.donation import donation_crud
from app.core.user import current_user
from app.core.utils import invest_funds

router = APIRouter()

@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    dependencies=[Depends(invest_funds)]
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    return DonationUserSchema.from_orm(new_donation)

@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    if user.is_superuser:
        all_projects = await donation_crud.get_multi(session)
        return all_projects
    all_projects = await donation_crud.get_by_user(
        session=session, user=user
    )
    return all_projects

