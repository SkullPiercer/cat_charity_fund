from datetime import datetime

from fastapi import HTTPException
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
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    room_id = await projects_crud.get_project_id_by_name(project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.invested_amount != 0 or project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='В проект уже внесены средства!',
        )
    return project


async def check_project_full_amount(
        project: CharityProject,
        obj_full_amount: int,
        session: AsyncSession
) -> CharityProject:
    if obj_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже внесённой!',
        )
    elif obj_full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
        session.add(project)
        await session.commit()
        await session.refresh(project)
    return project