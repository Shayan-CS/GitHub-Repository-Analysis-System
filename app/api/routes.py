from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schemas, services
from app.db.session import get_async_session

router = APIRouter()


@router.post("/repositories", response_model=schemas.RepositoryOut, status_code=201)
async def create_repository(repo_in: schemas.RepositoryCreate, session: AsyncSession = Depends(get_async_session)):
    repo = await services.create_repository(session, repo_in)
    return repo


@router.get("/repositories", response_model=list[schemas.RepositoryOut])
async def list_repositories(limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    repos = await services.list_repositories(session, limit=limit)
    return repos


@router.get("/repositories/{repo_id}", response_model=schemas.RepositoryOut)
async def get_repository(repo_id: str, session: AsyncSession = Depends(get_async_session)):
    repo = await services.get_repository(session, repo_id)
    if repo is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo
