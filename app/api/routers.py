from fastapi import APIRouter

from app.api.endpoints import user_router, projects_router

main_router = APIRouter()

main_router.include_router(
    projects_router, prefix='/projects', tags=['Projects']
)
main_router.include_router(user_router)