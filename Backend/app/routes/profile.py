"""CRUD routes for user profiles."""
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models.schemas import UserProfileCreate, UserProfileUpdate, UserProfileResponse

router = APIRouter(prefix="/profiles", tags=["profiles"])
profiles_db = {}


def _profile_to_response(profile: dict) -> UserProfileResponse:
    """Convert profile dict to response schema."""
    return UserProfileResponse(
        id=profile["id"],
        name=profile["name"],
        skills=profile["skills"],
        resume_text=profile.get("resume_text"),
        target_role_id=profile.get("target_role_id"),
        created_at=profile["created_at"],
        updated_at=profile["updated_at"],
    )


@router.post("", response_model=UserProfileResponse, status_code=201)
def create_profile(data: UserProfileCreate):
    """Create a new user profile."""
    if not data.name or not data.name.strip():
        raise HTTPException(status_code=400, detail="Name must not be empty")
    if not data.skills or len(data.skills) < 1:
        raise HTTPException(status_code=400, detail="At least one skill is required")

    profile_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    profile = {
        "id": profile_id,
        "name": data.name.strip(),
        "skills": data.skills,
        "resume_text": data.resume_text,
        "target_role_id": data.target_role_id,
        "created_at": now,
        "updated_at": now,
    }
    profiles_db[profile_id] = profile
    return _profile_to_response(profile)


@router.get("", response_model=list)
def list_profiles(search: Optional[str] = None):
    """List all profiles, optionally filtered by name search."""
    if not search:
        return [_profile_to_response(p) for p in profiles_db.values()]

    search_lower = search.lower()
    filtered = [
        _profile_to_response(p)
        for p in profiles_db.values()
        if search_lower in p["name"].lower()
    ]
    return filtered


@router.get("/{profile_id}", response_model=UserProfileResponse)
def get_profile(profile_id: str):
    """Get a single profile by ID."""
    if profile_id not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")
    return _profile_to_response(profiles_db[profile_id])


@router.put("/{profile_id}", response_model=UserProfileResponse)
def update_profile(profile_id: str, data: UserProfileUpdate):
    """Update a profile. Only provided fields are updated."""
    if profile_id not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile = profiles_db[profile_id]
    now = datetime.now(timezone.utc).isoformat()

    if data.name is not None:
        profile["name"] = data.name
    if data.skills is not None:
        profile["skills"] = data.skills
    if data.resume_text is not None:
        profile["resume_text"] = data.resume_text
    if data.target_role_id is not None:
        profile["target_role_id"] = data.target_role_id

    profile["updated_at"] = now
    return _profile_to_response(profile)


@router.delete("/{profile_id}")
def delete_profile(profile_id: str):
    """Delete a profile."""
    if profile_id not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")
    del profiles_db[profile_id]
    return {"message": "Profile deleted successfully"}
