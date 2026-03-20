"""Skill gap analysis routes."""
import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisRequest, SkillGapResult
from app.services.ai_service import AIService
from app.services.fallback_service import FallbackService
from app.services.data_service import DataService

router = APIRouter(prefix="/analysis", tags=["analysis"])
logger = logging.getLogger(__name__)
ai_service = AIService()
fallback_service = FallbackService()


def get_data_service() -> DataService:
    """Get DataService singleton."""
    return DataService()


@router.post("/analyze", response_model=SkillGapResult)
async def analyze_skills(request: AnalysisRequest):
    """
    Analyze user skills against a target role.
    Uses AI if available and use_ai=True, otherwise falls back to rule-based analysis.
    """
    data_service = get_data_service()
    role = data_service.get_role_by_id(request.target_role_id)

    if role is None:
        raise HTTPException(status_code=400, detail="Invalid role ID. Role not found.")

    if not request.user_skills:
        raise HTTPException(status_code=400, detail="At least one skill is required for analysis")

    analysis_mode = "fallback"
    result_base = None

    if request.use_ai and ai_service.is_available():
        try:
            ai_result = await ai_service.analyze_skills(
                user_skills=request.user_skills,
                resume_text=request.resume_text or "",
                role=role,
            )
            analysis_mode = "ai"
            # Merge user-provided skills with AI-extracted; use canonical casing, case-insensitive dedupe
            extracted = ai_result.get("extracted_skills", []) or []
            required_skills = [s for s in (role.get("required_skills") or []) if s and isinstance(s, str) and str(s).strip()]
            preferred_skills = [s for s in (role.get("preferred_skills") or []) if s and isinstance(s, str) and str(s).strip()]
            ref_skills = required_skills + preferred_skills
            raw_skills = (
                [s for s in (request.user_skills or []) if s and isinstance(s, str) and str(s).strip()] +
                [s for s in extracted if s and isinstance(s, str) and str(s).strip()]
            )
            all_user_skills = fallback_service.dedupe_skills_canonical(
                [fallback_service.normalize_skill(s) for s in raw_skills],
                ref_skills
            )
            # Compute matching/missing deterministically from our canonical role skills
            # (AI may return different skill names e.g. "Amazon Web Services" vs "AWS")
            user_skills_lower = {s.lower() for s in all_user_skills}
            matching_skills = [s for s in required_skills if s.lower() in user_skills_lower]
            missing_skills = [s for s in required_skills if s.lower() not in user_skills_lower]
            match_percentage = (
                round((len(matching_skills) / len(required_skills)) * 100, 1)
                if required_skills else 0.0
            )
            # Map AI priority_skills to our canonical names; preserve AI order when possible
            ai_priority = ai_result.get("priority_skills", [])
            priority_skills = []
            for p in ai_priority:
                if not p or not str(p).strip():
                    continue
                norm = fallback_service.normalize_skill(p)
                for m in missing_skills:
                    if m.lower() == norm.lower() and m not in priority_skills:
                        priority_skills.append(m)
                        break
            for m in missing_skills:
                if m not in priority_skills:
                    priority_skills.append(m)
            # Normalize learning_roadmap skill names to our canonical role skills
            roadmap = ai_result.get("learning_roadmap", [])
            missing_lower = {s.lower(): s for s in missing_skills}
            for step in roadmap:
                skill = step.get("skill", "")
                norm = fallback_service.normalize_skill(skill).lower()
                if norm in missing_lower:
                    step["skill"] = missing_lower[norm]
            result_base = {
                "target_role": role["title"],
                "target_role_id": role["id"],
                "user_skills": all_user_skills,
                "required_skills": required_skills,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "match_percentage": match_percentage,
                "priority_skills": priority_skills[: min(5, len(priority_skills))],
                "learning_roadmap": roadmap,
                "ai_insights": ai_result.get("insights", ""),
                "analysis_mode": "ai",
            }
        except Exception as e:
            logger.error(f"AI analysis failed, falling back: {e}")
            result_base = None

    if result_base is None:
        result_base = fallback_service.analyze_skills(
            user_skills=request.user_skills,
            resume_text=request.resume_text,
            role=role,
        )
        analysis_mode = result_base.get("analysis_mode", "fallback")

    # Get course recommendations for missing skills
    missing = result_base.get("missing_skills", [])
    recommended_courses = data_service.get_courses_for_skills(missing)

    return SkillGapResult(
        target_role=result_base["target_role"],
        target_role_id=result_base["target_role_id"],
        user_skills=result_base["user_skills"],
        required_skills=result_base["required_skills"],
        matching_skills=result_base["matching_skills"],
        missing_skills=result_base["missing_skills"],
        match_percentage=result_base["match_percentage"],
        recommended_courses=recommended_courses,
        learning_roadmap=result_base["learning_roadmap"],
        analysis_mode=analysis_mode,
        ai_insights=result_base.get("ai_insights"),
        priority_skills=result_base.get("priority_skills", []),
    )


@router.get("/sample/{resume_id}/{role_id}", response_model=SkillGapResult)
def get_sample_analysis(resume_id: str, role_id: str):
    """Run fallback analysis on a sample resume against a role. Quick demo endpoint."""
    data_service = get_data_service()
    resume = data_service.get_resume_by_id(resume_id)
    role = data_service.get_role_by_id(role_id)

    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    result = fallback_service.analyze_skills(
        user_skills=resume.get("skills", []),
        resume_text=resume.get("resume_text"),
        role=role,
    )
    recommended_courses = data_service.get_courses_for_skills(result["missing_skills"])

    return SkillGapResult(
        target_role=result["target_role"],
        target_role_id=result["target_role_id"],
        user_skills=result["user_skills"],
        required_skills=result["required_skills"],
        matching_skills=result["matching_skills"],
        missing_skills=result["missing_skills"],
        match_percentage=result["match_percentage"],
        recommended_courses=recommended_courses,
        learning_roadmap=result["learning_roadmap"],
        analysis_mode="fallback",
        ai_insights=result.get("ai_insights"),
        priority_skills=result.get("priority_skills", []),
    )
