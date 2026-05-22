from typing import Any

from fastapi import APIRouter, Depends

from app.db.mongo import get_db
from app.models.schemas import OverviewResponse

router = APIRouter(prefix="/analytics")


@router.get("/org/{org_name}/overview", response_model=OverviewResponse)
async def org_overview(org_name: str, db: Any = Depends(get_db)) -> OverviewResponse:
    repo_count = await db.repos.count_documents({"org_login": org_name})
    open_issues_count = await db.issues.count_documents({"org_login": org_name, "state": "open"})
    team_count = await db.teams.count_documents({"org_login": org_name})
    member_count = await db.users.count_documents({"org_login": org_name})

    return OverviewResponse(
        org_name=org_name,
        repo_count=repo_count,
        open_issues_count=open_issues_count,
        team_count=team_count,
        member_count=member_count,
    )
