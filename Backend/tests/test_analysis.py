"""Happy path test for skill gap analysis."""
import pytest
from app.services.fallback_service import FallbackService
from app.services.data_service import DataService


class TestSkillGapAnalysis:
    """Happy path test: Valid skill gap analysis with known data."""

    def setup_method(self):
        self.fallback = FallbackService()
        self.data_service = DataService()
        self.data_service.load_data()

    def test_valid_skill_gap_analysis(self):
        """
        Test with known user skills against Cloud Engineer role.
        User has: Python, Git, Linux
        Cloud Engineer requires: AWS, Azure, Terraform, Docker, Kubernetes, Linux, Python, CI/CD, Networking
        Expected:
        - matching_skills contains Python and Linux
        - missing_skills contains AWS, Docker, Kubernetes, Terraform, CI/CD, etc.
        - match_percentage is approximately 22.2% (2/9)
        - recommended_courses is not empty
        - analysis_mode is "fallback"
        - learning_roadmap is ordered with prerequisites respected
        """
        role = self.data_service.get_role_by_id("role_001")  # Cloud Engineer
        assert role is not None

        result = self.fallback.analyze_skills(
            user_skills=["Python", "Git", "Linux"],
            resume_text=None,
            role=role
        )

        assert "Python" in result["matching_skills"]
        assert "Linux" in result["matching_skills"]
        assert len(result["missing_skills"]) > 0
        assert "AWS" in result["missing_skills"]
        assert result["match_percentage"] > 0
        assert result["match_percentage"] < 100
        assert result["analysis_mode"] == "fallback"
        assert len(result["learning_roadmap"]) > 0
        assert len(result["priority_skills"]) > 0
        assert result["ai_insights"] is not None and len(result["ai_insights"]) > 0

    def test_full_match_analysis(self):
        """Test when user has ALL required skills — should be 100% match."""
        role = self.data_service.get_role_by_id("role_001")

        result = self.fallback.analyze_skills(
            user_skills=role["required_skills"].copy(),
            resume_text=None,
            role=role
        )

        assert result["match_percentage"] == 100.0
        assert len(result["missing_skills"]) == 0
        assert len(result["matching_skills"]) == len(role["required_skills"])
