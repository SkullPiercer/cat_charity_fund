from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.projects import CharityProjectDB, CharityProjectCreate
from app.crud.projects import projects_crud

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