from app.crud.base import CRUDBase
from app.models import Project

class CRUDProjects(CRUDBase):
    ...

projects_crud = CRUDProjects(Project)