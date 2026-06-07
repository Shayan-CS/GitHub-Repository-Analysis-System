import httpx
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


async def fetch_repo_readme(owner: str, repo: str) -> Optional[str]:
    headers = {}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        r = await client.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            import base64

            content = base64.b64decode(data.get("content", "")).decode(errors="ignore")
            return content
        logger.warning("Failed to fetch README %s/%s status=%s", owner, repo, r.status_code)
        return None


async def fetch_repo_metadata(owner: str, repo: str) -> dict:
    headers = {}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    url = f"https://api.github.com/repos/{owner}/{repo}"
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        r = await client.get(url)
        if r.status_code == 200:
            return r.json()
        logger.warning("Failed to fetch repo metadata %s/%s status=%s", owner, repo, r.status_code)
        return {}
