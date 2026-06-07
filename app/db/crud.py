from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import models
from app.api import schemas


async def create_repository(session: AsyncSession, repo_in: schemas.RepositoryCreate) -> models.Repository:
    repo = models.Repository(
        github_url=str(repo_in.github_url),
        name=repo_in.github_url.path.strip("/"),
        description=repo_in.description,
    )
    session.add(repo)
    await session.commit()
    await session.refresh(repo)
    return repo


async def get_repository(session: AsyncSession, repo_id: str) -> Optional[models.Repository]:
    q = select(models.Repository).where(models.Repository.id == repo_id)
    result = await session.execute(q)
    return result.scalars().first()


async def list_repositories(session: AsyncSession, limit: int = 100) -> List[models.Repository]:
    q = select(models.Repository).order_by(models.Repository.created_at.desc()).limit(limit)
    result = await session.execute(q)
    return result.scalars().all()


async def create_analysis(session: AsyncSession, repository_id: str, summary: str, complexity_score: float, topics: list, embedding_id: str | None = None) -> models.Analysis:
    analysis = models.Analysis(
        repository_id=repository_id,
        summary=summary,
        complexity_score=complexity_score,
        topics=topics,
        embedding_id=embedding_id,
    )
    session.add(analysis)
    await session.commit()
    await session.refresh(analysis)
    return analysis


async def get_analysis_by_repository(session: AsyncSession, repository_id: str):
    q = select(models.Analysis).where(models.Analysis.repository_id == repository_id)
    result = await session.execute(q)
    return result.scalars().first()
