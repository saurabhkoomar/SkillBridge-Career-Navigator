"""Singleton service that loads and queries JSON data files."""
import json
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class DataService:
    """Singleton service that loads and queries JSON data files."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.resumes: List[Dict] = []
        self.job_roles: List[Dict] = []
        self.courses: List[Dict] = []
        self._initialized = True

    def load_data(self):
        """Load all JSON data files from the data directory."""
        # __file__ is app/services/data_service.py -> go up to backend/ then data/
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_dir = os.path.join(backend_dir, "data")

        try:
            with open(os.path.join(data_dir, "resumes.json"), "r", encoding="utf-8") as f:
                self.resumes = json.load(f)
            logger.info(f"Loaded {len(self.resumes)} resumes")

            with open(os.path.join(data_dir, "job_roles.json"), "r", encoding="utf-8") as f:
                self.job_roles = json.load(f)
            logger.info(f"Loaded {len(self.job_roles)} job roles")

            with open(os.path.join(data_dir, "courses.json"), "r", encoding="utf-8") as f:
                self.courses = json.load(f)
            logger.info(f"Loaded {len(self.courses)} courses")

        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file: {e}")
            raise

    def get_role_by_id(self, role_id: str) -> Optional[Dict]:
        """Return a job role by ID or None."""
        for role in self.job_roles:
            if role["id"] == role_id:
                return role
        return None

    def get_resume_by_id(self, resume_id: str) -> Optional[Dict]:
        """Return a resume by ID or None."""
        for resume in self.resumes:
            if resume["id"] == resume_id:
                return resume
        return None

    def search_roles(self, keyword=None, industry=None, experience_level=None, skill=None) -> List[Dict]:
        """Filter roles by any combination of parameters. All filters are case-insensitive."""
        results = self.job_roles.copy()

        if keyword:
            keyword_lower = keyword.lower()
            results = [r for r in results if keyword_lower in r["title"].lower() or keyword_lower in r["description"].lower()]

        if industry:
            results = [r for r in results if r.get("industry", "").lower() == industry.lower()]

        if experience_level:
            results = [r for r in results if r.get("experience_level", "").lower() == experience_level.lower()]

        if skill:
            skill_lower = skill.lower()
            results = [r for r in results if
                       any(s.lower() == skill_lower for s in r.get("required_skills", [])) or
                       any(s.lower() == skill_lower for s in r.get("preferred_skills", []))]

        return results

    def get_courses_for_skills(self, skills: list) -> List[Dict]:
        """Return courses that cover any of the given skills. Sorted by rating descending."""
        if not skills:
            return []

        skills_lower = {s.lower() for s in skills}
        matching_courses = []

        for course in self.courses:
            if course.get("skill_covered", "").lower() in skills_lower:
                matching_courses.append(course)
            elif any(s.lower() in skills_lower for s in course.get("related_skills", [])):
                matching_courses.append(course)

        matching_courses.sort(key=lambda c: c.get("rating", 0), reverse=True)
        return matching_courses

    def get_all_roles(self) -> List[Dict]:
        """Return all job roles."""
        return self.job_roles

    def get_all_courses(self) -> List[Dict]:
        """Return all courses."""
        return self.courses

    def get_all_resumes(self) -> List[Dict]:
        """Return all resumes."""
        return self.resumes
