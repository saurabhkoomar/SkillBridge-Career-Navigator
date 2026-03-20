"""Rule-based skill gap analysis without AI/API - fallback when Groq is unavailable."""
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class FallbackService:
    """
    Rule-based skill gap analysis that works without any AI/API.
    This is the fallback when Groq is unavailable, API key is missing, or AI returns an error.
    Uses keyword matching, skill normalization, and predefined priority rules.
    """

    SKILL_ALIASES = {
        "js": "JavaScript", "javascript": "JavaScript",
        "ts": "TypeScript", "typescript": "TypeScript",
        "py": "Python", "python": "Python",
        "react.js": "React", "reactjs": "React", "react": "React",
        "node": "Node.js", "nodejs": "Node.js", "node.js": "Node.js",
        "k8s": "Kubernetes", "kubernetes": "Kubernetes",
        "aws": "AWS", "amazon web services": "AWS", "amazon web services (aws)": "AWS",
        "gcp": "GCP", "google cloud": "GCP", "google cloud platform": "GCP",
        "azure": "Azure", "microsoft azure": "Azure",
        "ml": "Machine Learning", "machine learning": "Machine Learning",
        "ai": "Artificial Intelligence",
        "ci/cd": "CI/CD", "cicd": "CI/CD", "ci cd": "CI/CD",
        "postgres": "SQL", "postgresql": "SQL", "mysql": "SQL", "sql": "SQL",
        "mongo": "NoSQL", "mongodb": "NoSQL", "nosql": "NoSQL",
        "docker": "Docker", "terraform": "Terraform",
        "linux": "Linux", "ubuntu": "Linux", "centos": "Linux",
        "git": "Git", "github": "Git", "gitlab": "Git",
        "html": "HTML", "css": "CSS",
        "flask": "Flask", "django": "Django",
        "express": "Express", "expressjs": "Express",
        "figma": "Figma", "tailwind": "Tailwind CSS",
        "redux": "Redux", "graphql": "GraphQL",
        "ansible": "Ansible", "jenkins": "Jenkins",
        "tensorflow": "TensorFlow", "pytorch": "PyTorch",
        "pandas": "Pandas", "numpy": "NumPy",
        "scikit-learn": "Scikit-learn", "sklearn": "Scikit-learn",
        "tableau": "Tableau", "power bi": "Power BI",
        "wireshark": "Wireshark", "nmap": "Nmap",
        "siem": "SIEM", "firewalls": "Firewalls",
        "rest": "REST APIs", "rest api": "REST APIs", "rest apis": "REST APIs",
        "microservices": "Microservices", "system design": "System Design",
        "data visualization": "Data Visualization", "responsive design": "Responsive Design",
        "security frameworks": "Security Frameworks", "incident response": "Incident Response",
        "threat analysis": "Threat Analysis", "testing": "Testing", "statistics": "Statistics",
        "math/statistics": "Math/Statistics",
        "cloud security": "Cloud Security", "compliance": "Compliance",
        "serverless": "Serverless", "prometheus": "Prometheus", "grafana": "Grafana",
        "excel": "Excel", "communication": "Communication", "problem solving": "Problem Solving",
        "data analysis": "Data Analysis", "message queues": "Message Queues",
        "apache spark": "Apache Spark", "data modeling": "Data Modeling",
        "next.js": "Next.js", "etl": "ETL", "math": "Math/Statistics", "mathematics": "Math/Statistics",
    }

    SKILL_PRIORITY = {
        "Python": 9, "AWS": 9, "Docker": 8, "Kubernetes": 8,
        "Linux": 8, "Git": 7, "CI/CD": 8, "Terraform": 8,
        "JavaScript": 8, "React": 7, "Node.js": 7, "SQL": 8,
        "TypeScript": 7, "System Design": 9, "Networking": 7,
        "Machine Learning": 8, "Cybersecurity": 8, "Azure": 7,
        "Java": 7, "REST APIs": 7, "NoSQL": 6, "GraphQL": 6,
        "Ansible": 6, "GCP": 7, "TensorFlow": 7, "PyTorch": 7,
        "Monitoring": 6, "Microservices": 7, "Data Visualization": 6,
        "Figma": 5, "HTML": 5, "CSS": 5, "Tailwind CSS": 5,
        "SIEM": 7, "Firewalls": 7, "Wireshark": 6,
        "Incident Response": 7, "Threat Analysis": 7,
        "Data Modeling": 7, "ETL": 7, "Apache Spark": 7,
        "Airflow": 6, "Statistics": 7, "Excel": 5,
        "Data Visualization": 6, "Responsive Design": 5, "Testing": 5,
    }

    SKILL_PREREQUISITES = {
        "Kubernetes": ["Docker"],
        "Terraform": ["AWS"],
        "React": ["JavaScript"],
        "Node.js": ["JavaScript"],
        "TypeScript": ["JavaScript"],
        "Redux": ["React"],
        "Machine Learning": ["Python"],
        "TensorFlow": ["Python", "Machine Learning"],
        "PyTorch": ["Python", "Machine Learning"],
        "Ansible": ["Linux"],
        "CI/CD": ["Git"],
        "GCP": ["AWS"],
        "Azure": ["AWS"],
        "Scikit-learn": ["Python"],
        "Apache Spark": ["Python", "SQL"],
        "Airflow": ["Python"],
        "Express": ["Node.js", "JavaScript"],
        "Django": ["Python"],
        "Flask": ["Python"],
        "GraphQL": ["REST APIs"],
        "Microservices": ["Docker", "REST APIs"],
        "Service Mesh": ["Kubernetes"],
        "GitOps": ["Git", "Kubernetes"],
    }

    def normalize_skill(self, skill: str) -> str:
        """
        Normalize a skill name using alias mapping. Case-insensitive.
        Returns canonical form from SKILL_ALIASES, or stripped input for unknowns.
        """
        if not skill or not isinstance(skill, str):
            return ""
        s = skill.strip()
        cleaned = s.lower()
        if cleaned in self.SKILL_ALIASES:
            return self.SKILL_ALIASES[cleaned]
        return s

    def get_canonical_casing(
        self, skill: str, reference_skills: Optional[List[str]] = None
    ) -> str:
        """
        Return the canonical casing for a skill.
        Priority: 1) exact match in reference_skills (role's required/preferred)
                  2) SKILL_ALIASES
                  3) SKILL_PRIORITY keys
                  4) title case for multi-word unknowns; as-is for single-word
        """
        if not skill or not isinstance(skill, str):
            return ""
        s = skill.strip()
        if not s:
            return ""
        cleaned = s.lower()
        if reference_skills:
            for ref in reference_skills:
                if ref and ref.lower() == cleaned:
                    return ref
        if cleaned in self.SKILL_ALIASES:
            return self.SKILL_ALIASES[cleaned]
        for canonical in self.SKILL_PRIORITY:
            if canonical and canonical.lower() == cleaned:
                return canonical
        # Unknown skill: use title case for multi-word to reduce casing drift
        if " " in s and s.islower():
            return s.title()
        return s

    def dedupe_skills_canonical(
        self, skills: List[str], reference_skills: Optional[List[str]] = None
    ) -> List[str]:
        """
        Deduplicate skills case-insensitively, using canonical casing.
        Returns list with no duplicates (by lowercase) and consistent casing.
        """
        seen_lower = {}
        ref_list = reference_skills or []
        result = []
        for skill in skills:
            if not skill or not str(skill).strip():
                continue
            cleaned = str(skill).lower().strip()
            if cleaned in seen_lower:
                continue
            canonical = self.get_canonical_casing(skill, ref_list)
            seen_lower[cleaned] = canonical
            result.append(canonical)
        return result

    def extract_skills_from_resume(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text using keyword matching.
        Searches for all known skill names in the text.
        Returns list of unique normalized skills found.
        """
        if not resume_text:
            return []

        found_skills = set()
        text_lower = resume_text.lower()

        # Check all known skills
        all_known_skills = set(self.SKILL_ALIASES.values()) | set(self.SKILL_PRIORITY.keys())

        for skill in all_known_skills:
            if skill.lower() in text_lower:
                found_skills.add(skill)

        # Also check alias keys
        for alias, normalized in self.SKILL_ALIASES.items():
            if alias in text_lower:
                found_skills.add(normalized)

        return list(found_skills)

    def analyze_skills(self, user_skills: list, resume_text: Optional[str], role: dict) -> dict:
        """
        Complete rule-based skill gap analysis.

        Steps:
        1. Normalize all user skills
        2. Extract additional skills from resume text if provided
        3. Compare against role requirements
        4. Calculate match percentage
        5. Sort missing skills by priority
        6. Generate learning roadmap respecting prerequisites
        7. Generate text insights
        """
        # 1. Normalize and deduplicate user skills (case-insensitive, canonical casing)
        required_skills = role.get("required_skills", [])
        preferred_skills = role.get("preferred_skills", [])
        ref_skills = required_skills + preferred_skills

        normalized_user_skills = [
            self.get_canonical_casing(self.normalize_skill(s), ref_skills)
            for s in (user_skills or [])
            if s and str(s).strip()
        ]

        # 2. Extract from resume and merge (with canonical casing, case-insensitive dedupe)
        if resume_text:
            resume_skills = self.extract_skills_from_resume(resume_text)
            all_user_skills = self.dedupe_skills_canonical(
                normalized_user_skills + resume_skills, ref_skills
            )
        else:
            all_user_skills = self.dedupe_skills_canonical(
                normalized_user_skills, ref_skills
            )

        # 3. Role skills (use exact casing from role data)

        # 4. Compare (case-insensitive); matching/missing use role's exact casing
        user_skills_lower = {s.lower() for s in all_user_skills}

        matching = [
            req for req in required_skills
            if req and req.lower() in user_skills_lower
        ]
        missing = [
            req for req in required_skills
            if req and req.lower() not in user_skills_lower
        ]

        # Match percentage
        if required_skills:
            match_pct = round((len(matching) / len(required_skills)) * 100, 1)
        else:
            match_pct = 0.0

        # 5. Sort missing by priority
        missing_sorted = sorted(missing, key=lambda s: self.SKILL_PRIORITY.get(s, 5), reverse=True)

        # Priority skills = top 3-5
        priority_skills = missing_sorted[:min(5, len(missing_sorted))]

        # 6. Generate learning roadmap with prerequisites
        roadmap = self._generate_roadmap(missing_sorted, all_user_skills, role['title'])

        # 7. Generate insights
        insights = self._generate_insights(matching, missing_sorted, match_pct, role['title'], priority_skills)

        return {
            "target_role": role["title"],
            "target_role_id": role["id"],
            "user_skills": all_user_skills,
            "required_skills": required_skills,
            "matching_skills": matching,
            "missing_skills": missing_sorted,
            "match_percentage": match_pct,
            "priority_skills": priority_skills,
            "learning_roadmap": roadmap,
            "ai_insights": insights,
            "analysis_mode": "fallback",
            "extracted_skills": [s for s in all_user_skills if s not in normalized_user_skills]
        }

    def _generate_roadmap(self, missing_skills: list, user_skills: list, role_title: str) -> list:
        """Generate an ordered learning roadmap respecting prerequisites."""
        roadmap = []
        scheduled = set()
        order = 1

        def add_to_roadmap(skill):
            nonlocal order
            if skill in scheduled:
                return

            # Check prerequisites first
            prereqs = self.SKILL_PREREQUISITES.get(skill, [])
            user_skills_lower = {s.lower() for s in user_skills}
            for prereq in prereqs:
                if prereq.lower() not in user_skills_lower and prereq not in scheduled:
                    add_to_roadmap(prereq)

            priority = self.SKILL_PRIORITY.get(skill, 5)
            if priority >= 8:
                weeks = 2
                difficulty = "Intermediate"
            elif priority >= 6:
                weeks = 3
                difficulty = "Intermediate"
            else:
                weeks = 4
                difficulty = "Beginner"

            prereq_names = [p for p in self.SKILL_PREREQUISITES.get(skill, []) if p in scheduled]
            if prereq_names:
                reason = f"Builds on {', '.join(prereq_names)}. Required for {role_title} position."
            else:
                reason = f"Core requirement for {role_title}. High impact on your employability."

            roadmap.append({
                "order": order,
                "skill": skill,
                "reason": reason,
                "estimated_weeks": weeks,
                "difficulty": difficulty
            })
            scheduled.add(skill)
            order += 1

        for skill in missing_skills:
            add_to_roadmap(skill)

        return roadmap

    def _generate_insights(self, matching: list, missing: list, match_pct: float, role_title: str, priority: list) -> str:
        """Generate human-readable text insights."""
        total_weeks = sum(
            2 if self.SKILL_PRIORITY.get(s, 5) >= 8 else 3 if self.SKILL_PRIORITY.get(s, 5) >= 6 else 4
            for s in missing
        )

        if match_pct >= 75:
            strength = "You're a strong match"
            tone = "You're well-positioned for this role!"
        elif match_pct >= 50:
            strength = "You have a solid foundation"
            tone = "With focused learning, you can become a strong candidate."
        elif match_pct >= 25:
            strength = "You have some relevant skills"
            tone = "A structured learning plan will help you bridge the gap."
        else:
            strength = "You're at the beginning of your journey"
            tone = "Everyone starts somewhere — a focused roadmap will get you there."

        matching_str = ', '.join(matching[:3]) if matching else "None yet"
        priority_str = ', '.join(priority[:3]) if priority else "None"

        return (
            f"{strength} for the {role_title} role with a {match_pct}% skill match. "
            f"Your strongest matches are: {matching_str}. "
            f"To improve your profile, prioritize learning: {priority_str}. "
            f"Estimated time to fill critical gaps: {total_weeks} weeks. {tone}"
        )
