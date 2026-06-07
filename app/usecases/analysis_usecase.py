import asyncio
import logging
from typing import Optional

from app.services_ext.github_client import fetch_repo_metadata, fetch_repo_readme
from app.services_ext.embedding import embedding_client
from app.services_ext.llm import call_llm_for_analysis
from app.db import crud

logger = logging.getLogger(__name__)


async def analyze_repository(session, repository):
    # repository is ORM object with `name` in owner/repo format or we parse from github_url
    # parse owner and repo
    if "/" in repository.name:
        owner, repo = repository.name.split("/", 1)
    else:
        owner = repository.name
        repo = repository.name

    # fetch metadata
    metadata = await fetch_repo_metadata(owner, repo)

    # fetch README
    readme = await fetch_repo_readme(owner, repo) or ""

    # prepare text chunks (simple: full readme)
    text = f"{metadata.get('description','')}\n\n{readme}"

    # embeddings
    vectors = embedding_client.embed_text([text])
    embedding_id = None

    # attempt to upsert into Chroma
    try:
        from app.services_ext.chroma_client import chroma_client
        chroma_client.upsert("github-repositories", ids=[repository.id], embeddings=vectors, metadatas=[{"repo": repository.name}])
        embedding_id = repository.id
    except Exception:
        logger.exception("Failed to upsert embedding into Chroma")

    # store analysis via LLM
    summary, complexity_score, topics = call_llm_for_analysis(text)

    analysis = await crud.create_analysis(session, repository.id, summary, complexity_score, topics, embedding_id)

    return analysis
