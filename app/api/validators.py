from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.projects import projects_crud
from app.models import Project

async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> Project:
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
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await projects_crud.get_project_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )

async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> Project:
    project = await check_project_exists(project_id, session)
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=422,
            detail='В проект уже внесены средства!',
        )
    return project
