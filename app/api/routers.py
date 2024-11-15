from fastapi import APIRouter

from app.api.endpoints import user_router, projects_router, donations_router

main_router = APIRouter()

main_router.include_router(
    projects_router, prefix='/projects', tags=['Projects']
)
main_router.include_router(
    donations_router, prefix='/donations', tags=['Projects']
)
main_router.include_router(user_router)