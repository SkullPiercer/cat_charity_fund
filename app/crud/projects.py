from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Project


class CRUDProjects(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(Project.id).where(
                Project.name == project_name
            )
        )
        return db_project_id.scalars().first()


projects_crud = CRUDProjects(Project)
