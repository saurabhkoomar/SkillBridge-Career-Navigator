"""Groq API integration for intelligent skill gap analysis."""
import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class AIService:
    """AI service using Groq (Llama 3) for skill analysis."""

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
        self.enabled = os.getenv("AI_ENABLED", "true").lower() == "true"

        if self.api_key and self.enabled:
            self.client = Groq(api_key=self.api_key)
            logger.info("Groq AI service initialized successfully")
        else:
            self.client = None
            logger.warning(
                "Groq AI service not available - missing API key or disabled"
            )

    def is_available(self) -> bool:
        """Check if AI service is configured and available."""
        return self.enabled and self.client is not None

    async def analyze_skills(self, user_skills: list, resume_text: str, role: dict) -> dict:
        """
        Use Groq (Llama 3) to perform intelligent skill gap analysis.
        Returns structured analysis with insights and learning roadmap.
        Raises Exception if AI call fails (so caller can fall back).
        """
        if not self.is_available():
            raise Exception("AI service is not available")

        try:
            system_prompt = """You are an expert career advisor AI. Your job is to analyze a candidate's skills and resume against a target job role and provide actionable career guidance.

Rules:
1. Be encouraging but honest about skill gaps
2. Prioritize skills by their impact on getting hired
3. Consider transferable skills and related experience
4. Always respond in valid JSON format only - no markdown, no code blocks, just pure JSON
5. Be specific about why each skill matters for the role"""

            user_prompt = f"""Analyze this candidate's profile against the target job role:

CANDIDATE SKILLS: {', '.join(user_skills)}

CANDIDATE RESUME:
{resume_text if resume_text else 'No resume provided - analyze based on skills list only'}

TARGET ROLE: {role['title']}
ROLE DESCRIPTION: {role['description']}
REQUIRED SKILLS: {', '.join(role['required_skills'])}
PREFERRED SKILLS: {', '.join(role.get('preferred_skills', []))}

Respond with this exact JSON structure:
{{
    "extracted_skills": ["list of additional skills you identified from the resume that weren't in the skills list"],
    "missing_skills": ["skills from required_skills that the candidate lacks"],
    "matching_skills": ["skills the candidate has that match required_skills"],
    "match_percentage": 0.0,
    "priority_skills": ["top 3-5 most impactful missing skills to learn first, ordered by importance"],
    "insights": "A detailed 3-4 sentence personalized analysis. Mention what the candidate is strong in, what they should focus on, and an encouraging note about their career path.",
    "learning_roadmap": [
        {{
            "order": 1,
            "skill": "Skill Name",
            "reason": "Why this skill matters and why learn it in this order",
            "estimated_weeks": 2,
            "difficulty": "Beginner/Intermediate/Advanced"
        }}
    ]
}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000,
                top_p=0.9
            )

            raw_content = response.choices[0].message.content.strip()

            # Clean up response - remove markdown code blocks if present
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.startswith("```"):
                raw_content = raw_content[3:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
            raw_content = raw_content.strip()

            result = json.loads(raw_content)

            # Validate required fields exist
            required_fields = ["missing_skills", "matching_skills", "match_percentage", "priority_skills", "insights", "learning_roadmap"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"AI response missing required field: {field}")

            logger.info(f"AI analysis completed successfully for role: {role['title']}")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            raise Exception(f"AI returned invalid JSON: {e}") from e
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            raise Exception(f"AI analysis failed: {str(e)}") from e
