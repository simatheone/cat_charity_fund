from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject
from app.models.user import User


async def check_charity_project_before_edit(
    project_id: int,
    session: AsyncSession,
    user: User
) -> CharityProject:
    charity_project = await charityproject_crud.get_project(
        obj_id=project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Данный проект не найден!'
        )
    if not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Обычный пользователь не может удалять проект!'
        )
    return charity_project
