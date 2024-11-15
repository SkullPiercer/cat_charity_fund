from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.projects import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
from app.crud.projects import projects_crud
from app.api.validators import check_project_exists

router = APIRouter()

@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    new_project = await projects_crud.create(project, session)
    return new_project

@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    meeting_room = await check_project_exists(
        project_id, session
    )

    # if obj_in.name is not None:
    #     await check_name_duplicate(obj_in.name, session)

    meeting_room = await projects_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room