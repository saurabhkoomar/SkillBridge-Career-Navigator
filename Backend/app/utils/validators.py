"""Input validation helpers for Skill-Bridge Career Navigator."""
from typing import Tuple, List, Optional


def validate_skills_list(skills: list) -> Tuple[bool, List[str], str]:
    """
    Validate and clean skills list.
    Returns (is_valid, cleaned_skills, error_message)
    """
    if not skills:
        return False, [], "At least one skill is required"

    if not isinstance(skills, list):
        return False, [], "Skills must be a list"

    # Clean skills
    cleaned = []
    for skill in skills:
        if isinstance(skill, str) and skill.strip():
            cleaned.append(skill.strip())

    if not cleaned:
        return False, [], "At least one valid skill is required"

    # Remove duplicates (case-insensitive)
    seen = set()
    unique = []
    for skill in cleaned:
        if skill.lower() not in seen:
            seen.add(skill.lower())
            unique.append(skill)

    if len(unique) > 50:
        return False, [], "Maximum 50 skills allowed"

    return True, unique, ""


def validate_resume_text(text: Optional[str]) -> Tuple[bool, str]:
    """
    Validate resume text if provided.
    Returns (is_valid, error_message)
    """
    if text is None or text == "":
        return True, ""  # Resume is optional

    if not isinstance(text, str):
        return False, "Resume text must be a string"

    text = text.strip()

    if len(text) < 50:
        return False, "Resume text must be at least 50 characters long"

    if len(text) > 10000:
        return False, "Resume text must not exceed 10,000 characters"

    # Check it contains some alphabetic characters
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count < 20:
        return False, "Resume text must contain meaningful content"

    return True, ""
