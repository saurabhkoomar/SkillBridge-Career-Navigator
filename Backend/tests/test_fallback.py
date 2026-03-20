"""Edge case tests for the fallback service."""
import pytest
from app.services.fallback_service import FallbackService


class TestFallbackEdgeCases:
    """Edge case tests for the fallback service."""

    def setup_method(self):
        self.fallback = FallbackService()
        self.sample_role = {
            "id": "role_test",
            "title": "Test Engineer",
            "description": "Test role",
            "required_skills": ["Python", "Docker", "AWS", "Linux"],
            "preferred_skills": ["Terraform"]
        }

    def test_skill_normalization(self):
        """Test that skill aliases are normalized correctly."""
        assert self.fallback.normalize_skill("js") == "JavaScript"
        assert self.fallback.normalize_skill("k8s") == "Kubernetes"
        assert self.fallback.normalize_skill("py") == "Python"
        assert self.fallback.normalize_skill("reactjs") == "React"
        assert self.fallback.normalize_skill("node") == "Node.js"

    def test_resume_skill_extraction(self):
        """Test skills extraction from resume text."""
        resume = "Experienced with Python, Docker, and AWS. Familiar with CI/CD pipelines and Linux administration."
        skills = self.fallback.extract_skills_from_resume(resume)

        assert "Python" in skills
        assert "Docker" in skills
        assert "AWS" in skills
        assert "Linux" in skills

    def test_empty_resume_extraction(self):
        """Test that empty resume returns empty list."""
        assert self.fallback.extract_skills_from_resume("") == []
        assert self.fallback.extract_skills_from_resume(None) == []

    def test_no_matching_skills(self):
        """Test when user has zero matching skills."""
        result = self.fallback.analyze_skills(
            user_skills=["Photoshop", "Illustrator", "InDesign"],
            resume_text=None,
            role=self.sample_role
        )

        assert result["match_percentage"] == 0.0
        assert len(result["matching_skills"]) == 0
        assert len(result["missing_skills"]) == len(self.sample_role["required_skills"])

    def test_case_insensitive_matching(self):
        """Test that skill matching is case-insensitive."""
        result = self.fallback.analyze_skills(
            user_skills=["python", "DOCKER", "aws"],
            resume_text=None,
            role=self.sample_role
        )

        assert result["match_percentage"] == 75.0  # 3 out of 4
        assert len(result["matching_skills"]) == 3

    def test_duplicate_skills_handled(self):
        """Test that duplicate skills are handled properly."""
        result = self.fallback.analyze_skills(
            user_skills=["Python", "python", "PYTHON", "Docker"],
            resume_text=None,
            role=self.sample_role
        )

        # Should not count Python 3 times
        assert result["match_percentage"] == 50.0  # 2 out of 4 (Python + Docker)

    def test_canonical_casing_in_matching_missing(self):
        """Test that matching_skills and missing_skills use role's exact casing."""
        result = self.fallback.analyze_skills(
            user_skills=["python", "docker", "aws", "LINUX"],
            resume_text=None,
            role=self.sample_role
        )
        # Role has: ["Python", "Docker", "AWS", "Linux"] - response must use that casing
        assert result["matching_skills"] == ["Python", "Docker", "AWS", "Linux"]
        assert result["missing_skills"] == []
        assert all(
            s in self.sample_role["required_skills"]
            for s in result["matching_skills"]
        )

    def test_canonical_casing_user_skills_dedupe(self):
        """Test that user_skills are deduplicated case-insensitively with canonical casing."""
        result = self.fallback.analyze_skills(
            user_skills=["PYTHON", "Python", "python", "Docker", "DOCKER"],
            resume_text=None,
            role=self.sample_role
        )
        # user_skills should have each skill once, with canonical casing
        user_skills = result["user_skills"]
        assert user_skills.count("Python") == 1
        assert user_skills.count("Docker") == 1
        assert "python" not in user_skills
        assert "PYTHON" not in user_skills

    def test_get_canonical_casing(self):
        """Test get_canonical_casing prioritizes reference (role) skills."""
        ref = ["Python", "AWS", "Math/Statistics"]
        assert self.fallback.get_canonical_casing("python", ref) == "Python"
        assert self.fallback.get_canonical_casing("PYTHON", ref) == "Python"
        assert self.fallback.get_canonical_casing("math/statistics", ref) == "Math/Statistics"
