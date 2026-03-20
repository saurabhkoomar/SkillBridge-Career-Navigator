"""Course recommendation routes."""
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.services.data_service import DataService

router = APIRouter(prefix="/courses", tags=["courses"])


def get_data_service() -> DataService:
    """Get DataService singleton."""
    return DataService()


@router.get("")
def list_courses(
    skill: Optional[str] = None,
    difficulty: Optional[str] = None,
    cost: Optional[str] = None,
    platform: Optional[str] = None,
):
    """List all courses with optional filters."""
    data_service = get_data_service()
    courses = data_service.get_all_courses()

    if skill:
        skill_lower = skill.lower()
        courses = [
            c for c in courses
            if c.get("skill_covered", "").lower() == skill_lower
            or any(s.lower() == skill_lower for s in c.get("related_skills", []))
        ]
    if difficulty:
        courses = [c for c in courses if c.get("difficulty", "").lower() == difficulty.lower()]
    if cost:
        cost_lower = cost.lower()
        if cost_lower == "free":
            courses = [c for c in courses if c.get("cost", "").lower() == "free"]
        elif cost_lower == "paid":
            courses = [c for c in courses if c.get("cost", "").lower() != "free"]
    if platform:
        platform_lower = platform.lower()
        courses = [c for c in courses if c.get("platform", "").lower() == platform_lower]

    return courses


@router.get("/recommend")
def recommend_courses(skills: Optional[str] = None):
    """Get course recommendations for comma-separated list of skills."""
    if not skills or not skills.strip():
        raise HTTPException(status_code=400, detail="Please provide skills parameter")

    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    if not skill_list:
        raise HTTPException(status_code=400, detail="Please provide skills parameter")

    data_service = get_data_service()
    courses = data_service.get_courses_for_skills(skill_list)
    return courses
