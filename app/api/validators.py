from datetime import datetime

from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.projects import projects_crud
from app.models import CharityProject


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await projects_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    room_id = await projects_crud.get_project_id_by_name(project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.invested_amount != 0 or project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект уже внесены средства!',
        )
    return project


async def check_project_full_amount(
    project: CharityProject,
    obj_full_amount: int,
    session: AsyncSession
):

    if obj_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже внесённой!',
        )

    if obj_full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
        session.add(project)
    return project