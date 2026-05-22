from pydantic import BaseModel


class OverviewResponse(BaseModel):
    org_name: str
    repo_count: int
    open_issues_count: int
    team_count: int
    member_count: int
