from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.projects import projects_crud
from app.models import Project

async def check_project_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> Project:
    meeting_room = await projects_crud.get(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room

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
