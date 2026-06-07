from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import schemas
from app.db import crud


async def create_repository(session: AsyncSession, repo_in: schemas.RepositoryCreate):
    return await crud.create_repository(session, repo_in)


async def get_repository(session: AsyncSession, repo_id: str):
    return await crud.get_repository(session, repo_id)


async def list_repositories(session: AsyncSession, limit: int = 100) -> List:
    return await crud.list_repositories(session, limit=limit)
