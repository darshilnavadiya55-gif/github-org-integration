from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class GitHubClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    async def _request(self, method: str, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        url = f"{settings.GITHUB_API_BASE}{endpoint}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(method, url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    async def exchange_code_for_token(self, code: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GITHUB_OAUTH_CALLBACK,
                },
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    async def get_authenticated_user(self) -> dict[str, Any]:
        return await self._request("GET", "/user")

    async def get_org(self, org_name: str) -> dict[str, Any]:
        return await self._request("GET", f"/orgs/{org_name}")

    async def list_org_repos(self, org_name: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/orgs/{org_name}/repos", params={"per_page": 100})

    async def list_org_members(self, org_name: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/orgs/{org_name}/members", params={"per_page": 100})

    async def list_org_teams(self, org_name: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/orgs/{org_name}/teams", params={"per_page": 100})

    async def list_repo_issues(self, owner: str, repo: str) -> list[dict[str, Any]]:
        return await self._request(
            "GET",
            f"/repos/{owner}/{repo}/issues",
            params={"state": "open", "per_page": 100},
        )
