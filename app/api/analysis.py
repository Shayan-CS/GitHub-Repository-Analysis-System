from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.db import crud
from app.usecases.analysis_usecase import analyze_repository
from app.api import schemas
from app.services_ext.embedding import embedding_client
from app.services_ext.chroma_client import chroma_client

router = APIRouter()


@router.post("/analyze/{repo_id}", response_model=schemas.AnalysisOut)
async def analyze_endpoint(repo_id: str, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session)):
    repo = await crud.get_repository(session, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    # Run analysis in background
    background_tasks.add_task(analyze_repository, session, repo)

    # Return current analysis if present
    analysis = await crud.get_analysis_by_repository(session, repo_id)
    if analysis:
        return analysis
    # else return placeholder
    return {"id": "", "repository_id": repo_id, "summary": "Analysis queued", "complexity_score": 0.0, "topics": [], "created_at": None}


@router.get("/search")
async def search(query: str):
    # Embed query and run vector search in ChromaDB
    q_emb = embedding_client.embed_query(query)
    results = chroma_client.query("github-repositories", q_emb, n_results=5)
    hits = []
    if results:
        ids = []
        # results expected to have 'ids' and possibly 'metadatas'
        try:
            ids = results.get('ids', [[]])[0]
        except Exception:
            ids = []
        # fetch repo and analysis for each id
        async def fetch_for_id(session, rid):
            repo = await crud.get_repository(session, rid)
            analysis = await crud.get_analysis_by_repository(session, rid)
            return {"repository": repo, "analysis": analysis}

        # we cannot access DB session here without dependency; return IDs and metadatas for client to fetch details
        for rid in ids:
            hits.append({"id": rid})
    return {"results": hits}
