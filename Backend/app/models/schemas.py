"""Pydantic schemas for Skill-Bridge Career Navigator API."""
from typing import List, Optional
from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
    """Schema for creating a user profile."""
    name: str = Field(..., min_length=2, max_length=100)
    skills: List[str] = Field(..., min_length=1)
    resume_text: Optional[str] = None
    target_role_id: Optional[str] = None


class UserProfileUpdate(BaseModel):
    """Schema for updating a user profile."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    skills: Optional[List[str]] = Field(None, min_length=1)
    resume_text: Optional[str] = None
    target_role_id: Optional[str] = None


class UserProfileResponse(BaseModel):
    """Schema for profile response."""
    id: str
    name: str
    skills: List[str]
    resume_text: Optional[str] = None
    target_role_id: Optional[str] = None
    created_at: str
    updated_at: str


class AnalysisRequest(BaseModel):
    """Schema for skill analysis request."""
    user_skills: List[str]
    resume_text: Optional[str] = None
    target_role_id: str
    use_ai: bool = True


class SkillGapResult(BaseModel):
    """Schema for skill gap analysis result."""
    target_role: str
    target_role_id: str
    user_skills: List[str]
    required_skills: List[str]
    matching_skills: List[str]
    missing_skills: List[str]
    match_percentage: float
    recommended_courses: List[dict]
    learning_roadmap: List[dict]
    analysis_mode: str
    ai_insights: Optional[str] = None
    priority_skills: List[str]


class RoleSearchQuery(BaseModel):
    """Schema for role search query params."""
    keyword: Optional[str] = None
    industry: Optional[str] = None
    experience_level: Optional[str] = None
    skill: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema for error response."""
    detail: str
