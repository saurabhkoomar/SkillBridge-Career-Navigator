"""Job roles listing and search routes."""
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.services.data_service import DataService

router = APIRouter(prefix="/roles", tags=["roles"])


def get_data_service() -> DataService:
    """Get DataService singleton."""
    return DataService()


@router.get("")
def list_roles(
    keyword: Optional[str] = None,
    industry: Optional[str] = None,
    experience_level: Optional[str] = None,
    skill: Optional[str] = None,
):
    """List all job roles with optional filters."""
    data_service = get_data_service()
    roles = data_service.search_roles(
        keyword=keyword,
        industry=industry,
        experience_level=experience_level,
        skill=skill,
    )
    return roles


@router.get("/{role_id}")
def get_role(role_id: str):
    """Get a single role by ID."""
    data_service = get_data_service()
    role = data_service.get_role_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
