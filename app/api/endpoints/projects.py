from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.projects import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)
from app.crud.projects import projects_crud
from app.crud.donation import donation_crud
from app.api.validators import (
    check_project_exists,
    check_name_duplicate,
    check_project_before_delete,
    check_project_full_amount,
)
from app.core.utils import invest
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await projects_crud.create(project, session)
    available_donations = await donation_crud.get_not_full_invested(session)
    await invest(
        source=new_project,
        targets=available_donations,
        session=session
    )

    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(
        project_id, session
    )

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя обновлять полностью проинвестированный проект!',
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        project = await check_project_full_amount(
            project=project,
            obj_full_amount=obj_in.full_amount,
            session=session
        )

    return await projects_crud.update(project, obj_in, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    all_projects = await projects_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_before_delete(project_id, session)
    return await projects_crud.remove(project, session)
