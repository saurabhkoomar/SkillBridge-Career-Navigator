# 🧭 Skill-Bridge Career Navigator

> AI-powered career navigation platform that analyzes your skills against job requirements and creates personalized learning roadmaps.

## Candidate Information
- **Candidate Name:** Saurabh Kumar
- **Scenario Chosen:** Scenario 2 — Skill-Bridge Career Navigator
- **Estimated Time Spent:** 2-3 Hours

---

## Design Documentation

### Problem Statement

Students and early-career professionals face a structural "skills gap" between what they learned in school and what employers actually require. Job boards display requirements in isolation; certification platforms display courses in isolation. Neither tells a candidate **what to learn, in what order, or why** — relative to a specific role they want.

Skill-Bridge solves this by taking a candidate's current skills (from a resume paste or manual entry) and a target role, then producing a ranked gap analysis and a step-by-step, prerequisite-aware learning roadmap backed by curated course recommendations.

---

### System Architecture

The application follows a standard **client-server architecture** with a clear separation between the React frontend, the FastAPI backend, and the data/AI layers.

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER (React)                      │
│                                                             │
│  ProfilePage ──► AnalysisPage ──► RoadmapPage               │
│  RolesPage                                                  │
│       │                  │                                  │
│       └──────── Axios HTTP calls ──────────────────────────►│
└─────────────────────────────────────────────────────────────┘
                            │
                     REST API (JSON)
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    FastAPI Backend                          │
│                                                             │
│  /api/profiles      /api/roles       /api/courses           │
│  /api/analysis      /api/data                               │
│                                                             │
│        ┌────────────────────────────────────┐               │
│        │           Analysis Router          │               │
│        │  ┌─────────────┐  ┌─────────────┐ │                │
│        │  │  AIService  │  │FallbackSvc  │ │                │
│        │  │ (Groq/Llama)│  │ (Rule-based)│ │                │
│        │  └──────┬──────┘  └──────┬──────┘ │                │
│        │         │  on failure    │         │               │
│        │         └────────────────┘         │               │
│        └────────────────────────────────────┘               │
│                                                             │
│        ┌────────────────────────────────────┐               │
│        │           DataService              │               │
│        │  job_roles.json  courses.json      │               │
│        │  resumes.json                      │               │
│        └────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

**Key architectural decision:** The AI layer is completely isolated behind a service interface. The Analysis Router calls `AIService.analyze()` first; if the call fails (missing key, rate limit, malformed response), it transparently falls back to `FallbackService.analyze_skills()` and sets `analysis_mode = "fallback"` in the response. The frontend reflects this mode to the user. This means the app is **fully functional with zero AI dependency** — the fallback is not a degraded mode, it is a first-class path.

---

### Component Breakdown

#### Backend (`/backend/app/`)

| Module | Responsibility |
|---|---|
| `main.py` | FastAPI app factory; mounts all routers; CORS config |
| `routers/profiles.py` | CRUD for in-memory candidate profiles |
| `routers/analysis.py` | POST `/analyze` — orchestrates AI or fallback; GET `/sample` for demo |
| `routers/roles.py` | GET job roles with keyword/industry/skill/experience filters |
| `routers/courses.py` | GET courses with skill/difficulty/cost/platform filters; recommendation endpoint |
| `routers/data.py` | Exposes raw sample resumes for the frontend demo picker |
| `services/ai_service.py` | Wraps Groq API (Llama 3); builds prompt; parses structured JSON response |
| `services/fallback_service.py` | Rule-based gap analysis: normalization, alias resolution, case-insensitive matching, deduplication, roadmap ordering |
| `services/data_service.py` | Loads and indexes JSON datasets on startup; provides typed getters |
| `models/schemas.py` | Pydantic models for all request/response shapes |
| `utils/validators.py` | Input validation helpers (skills list, resume text length) |

#### Frontend (`/frontend/src/`)

| Page / Component | Responsibility |
|---|---|
| `ProfilePage` | Create / view / update / delete candidate profiles |
| `RolesPage` | Browse and filter 12 job roles; select a target role |
| `AnalysisPage` | Submit skills + role → render gap analysis (radar chart, match %, tagged skills, AI insights, priority skills) |
| `RoadmapPage` | Render step-by-step learning roadmap with timeline and course recommendations |
| `ModeToggle` | UI switch between AI mode and Manual (fallback) mode |

---

### Data Model

All data is synthetic and stored as static JSON files in `/backend/data/`.

**Job Role** (`job_roles.json` — 12 entries)
```json
{
  "id": "role_001",
  "title": "Cloud Engineer",
  "industry": "Cloud & Infrastructure",
  "experience_level": "Mid",
  "description": "...",
  "required_skills": ["AWS", "Azure", "Terraform", "Docker", "Kubernetes", "Linux", "Python", "CI/CD", "Networking"],
  "preferred_skills": ["GCP", "Ansible", "Prometheus"]
}
```

**Course** (`courses.json` — 25 entries)
```json
{
  "id": "course_001",
  "title": "AWS Certified Solutions Architect",
  "platform": "Coursera",
  "skill": "AWS",
  "difficulty": "Intermediate",
  "cost": "Paid",
  "estimated_weeks": 8,
  "rating": 4.7,
  "url": "https://..."
}
```

**Resume** (`resumes.json` — 8 synthetic profiles)
```json
{
  "id": "resume_003",
  "name": "Marcus Williams",
  "background": "Marketing to Web Dev career switcher",
  "resume_text": "...",
  "skills": ["HTML", "CSS", "JavaScript", "Google Analytics"]
}
```

**Analysis Response** (runtime — not persisted)
```json
{
  "user_skills": ["Python", "Git", "Linux"],
  "matching_skills": ["Python", "Linux"],
  "missing_skills": ["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD", "Azure", "Networking"],
  "match_percentage": 22.2,
  "priority_skills": ["AWS", "Docker", "Kubernetes"],
  "learning_roadmap": [
    { "skill": "Docker", "reason": "Prerequisite for Kubernetes", "estimated_weeks": 3, "difficulty": "Beginner" },
    ...
  ],
  "recommended_courses": [...],
  "ai_insights": "...",
  "analysis_mode": "fallback"
}
```

---

### AI Integration Design

**AI Path (Groq / Llama 3)**

The `AIService` constructs a structured prompt containing:
1. The candidate's skills and any resume text
2. The role's required and preferred skills
3. An explicit instruction to return a JSON object matching the analysis response schema

The response is parsed and validated. If any required field is missing or the JSON is malformed, the service raises an exception and the router falls back automatically.

**Fallback Path (Rule-Based)**

`FallbackService` performs the same analysis deterministically:

1. **Skill normalization** — resolves aliases (`"k8s"→"Kubernetes"`, `"py"→"Python"`, `"js"→"JavaScript"`) using an exact-match alias dictionary. Substring matching was explicitly rejected to prevent false positives (e.g. `"java"` incorrectly matching inside `"javascript"`).
2. **Deduplication** — user-supplied skills are deduplicated case-insensitively; canonical casing is taken from the role's skill list where available, falling back to title-case.
3. **Gap computation** — matching and missing skills use the role's exact casing throughout the response.
4. **Roadmap ordering** — steps are ordered to respect soft prerequisites (e.g. Docker before Kubernetes) using a hardcoded prerequisite graph.
5. **Priority skills** — missing skills are ranked by frequency of appearance across all roles in the dataset as a proxy for market demand.
6. **Course mapping** — each missing skill is matched to the highest-rated course(s) in `courses.json` for that skill.

**Decision flow:**

```
POST /api/analysis/analyze
        │
        ├─ AI mode enabled AND GROQ_API_KEY present?
        │       │
        │      YES ──► AIService.analyze()
        │                    │
        │             Success? ──► return result (mode="ai")
        │                    │
        │             Failure? ──┐
        │                        │
        └─ NO                    ▼
                          FallbackService.analyze_skills()
                                 │
                          return result (mode="fallback")
```

---

### Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Frontend** | React 18 | Component model maps cleanly to Profile / Analysis / Roadmap pages; fast iteration |
| **Charting** | Recharts | Radar chart for skill coverage; minimal setup, composable API |
| **Backend** | FastAPI (Python) | Async-ready, automatic OpenAPI docs, native Pydantic integration for validation |
| **Validation** | Pydantic v2 | Schema-first request/response validation; descriptive error messages out of the box |
| **AI Provider** | Groq (Llama 3) | Free tier; low-latency inference; OpenAI-compatible SDK; no fine-tuning required |
| **Testing** | pytest | Standard Python test runner; `setup_method` for clean state per test |
| **Data Storage** | JSON files (in-memory) | No database setup required within timebox; sufficient for synthetic demo data |
| **HTTP Client** | Axios | Promise-based; consistent error handling across frontend API calls |

---

### Security Design

- `GROQ_API_KEY` is read exclusively from environment variables via `python-dotenv`. It is never hardcoded, logged, or returned in any API response.
- `.env` is in `.gitignore`. A `.env.example` with placeholder values is committed instead.
- CORS is configured in `main.py` to allow `localhost:3000` only (development). In production this would be restricted to the deployed frontend origin.
- All user input is validated through Pydantic schemas before reaching any service layer. Skills lists are bounded in length; resume text is bounded by character count.
- No authentication is implemented (noted as a known limitation). Profiles are in-memory and scoped to the server process lifetime.

---

### Key Design Decisions & Tradeoffs

| Decision | Alternative Considered | Reason Chosen |
|---|---|---|
| Exact alias matching in `normalize_skill()` | Substring / fuzzy matching | Avoids false positives (`"java"` ↔ `"javascript"`). Deterministic and auditable. |
| In-memory profile storage | SQLite / PostgreSQL | Eliminates DB setup within timebox. Acceptable for demo; noted as limitation. |
| Static JSON datasets | Live job board scraping | Complies with data safety requirement; no rate limits or ToS concerns. |
| Groq (Llama 3) for AI | OpenAI GPT-4 | Free tier available; sufficient response quality for structured JSON extraction. |
| Fallback as first-class path | Fallback as error state | App is fully usable without an API key. Reviewer can evaluate all features offline. |
| Role's casing as canonical | User-supplied casing | Ensures consistent display in UI; prevents `"python"` / `"Python"` / `"PYTHON"` appearing as separate skills in output. |

---

### Future Enhancements

Ordered by estimated value-to-effort ratio:

1. **Persistent storage** — Replace in-memory profiles with SQLite (zero-config) or PostgreSQL. Add user authentication (JWT) so profiles survive server restarts.
2. **GitHub API integration** — Parse a candidate's public repos; infer skills from languages, frameworks, and `README` keywords. Would significantly improve accuracy for developers.
3. **Expanded role dataset** — Grow from 12 to 50–100 roles covering broader industries (FinTech, HealthTech, Game Dev). Automate dataset refresh from a curated synthetic seed.
4. **Mock Interview Pivot** — Given a profile's missing skills, generate role-specific technical interview questions via the AI service. Candidates can self-assess readiness.
5. **Roadmap progress tracking** — Let candidates mark skills as "in progress" or "complete". Persist progress across sessions. Show a completion percentage over time.
6. **Production deployment** — Containerise with Docker Compose (frontend + backend). Deploy backend to Railway/Render; frontend to Vercel. Add a CI pipeline (GitHub Actions) running the pytest suite on every push.

---

## Requirements Compliance Matrix

### Step 2: Mandatory Requirements (All Scenarios)

| # | Requirement | Status | How It Is Achieved |
|---|-------------|--------|---------------------|
| **1** | **Core Flow:** One end-to-end flow (Create + View + Update or equivalent) + basic search/filter | ✅ Met | **Create/View/Update:** Profile CRUD — Create profile (`POST /api/profiles`), View list (`GET /api/profiles`), View single (`GET /api/profiles/{id}`), Update (`PUT /api/profiles/{id}`). **Search/Filter:** Profiles support `?search=` (name filter). Roles support `?keyword=`, `?industry=`, `?experience_level=`, `?skill=`. Courses support `?skill=`, `?difficulty=`, `?cost=`, `?platform=`. Frontend: ProfilePage (CRUD), RolesPage (search/filter), AnalysisPage, RoadmapPage. |
| **2** | **AI Integration + Fallback:** One AI capability (Summarize, Categorize, Extract, or Forecast) with manual/rule-based fallback when AI unavailable or incorrect | ✅ Met | **AI Capability:** Extract + Categorize — AI extracts skills from resume, analyzes skill gaps, categorizes matching vs missing skills, generates insights and learning roadmap. (`app/services/ai_service.py` — Groq/Llama 3). **Fallback:** Rule-based analysis when API key missing, AI disabled, or AI call fails (`app/services/fallback_service.py`). Mode toggle in UI lets user choose AI or Manual mode. |
| **3** | **Basic Quality:** Input validation, clear error messages, at least 2 tests (one happy path, one edge case) | ✅ Met | **Validation:** Pydantic schemas (`app/models/schemas.py`), `validators.py` (skills list, resume text). **Error messages:** `HTTPException` with `detail` (e.g. "Profile not found", "Invalid role ID", "At least one skill is required"). **Tests:** `test_analysis.py` (2 happy-path tests), `test_fallback.py` (6+ edge-case tests: skill normalization, empty resume, no matching skills, case insensitivity, duplicate skills, canonical casing). |
| **4** | **Data Safety:** Use synthetic data only. No live scraping. Include small sample CSV/JSON in repo | ✅ Met | **Synthetic Data:** All data is synthetic JSON in `backend/data/` — `resumes.json` (8 resumes), `job_roles.json` (12 roles), `courses.json` (25 courses). No scraping; no real personal data. |
| **5** | **Security:** Do not commit API keys. Use `.env` and provide `.env.example` | ✅ Met | **Secrets:** `GROQ_API_KEY` read from env. `.env` in `.gitignore`. `backend/.env.example` provided with placeholders. No keys committed. |

### Scenario 2: Skill-Bridge Career Navigator — Specific Alignment

| Requirement | Status | How It Is Achieved |
|-------------|--------|---------------------|
| **Problem Alignment** | ✅ Met | Addresses skills gap between academic knowledge and job requirements. Platform uses resume/skill input and provides personalized learning roadmap. |
| **Target: Recent Graduates** | ✅ Met | 8 synthetic resumes include CS grads, data science students, bootcamp grads. Course recommendations and roadmap tailored to certifications and competitiveness. |
| **Target: Career Switchers** | ✅ Met | Synthetic resume #3 (Marcus Williams) — marketing to web dev. Fallback extracts transferable skills; roadmap respects prerequisites for role transitions. |
| **Target: Mentors** | ✅ Met | Data-backed analysis: match %, matching/missing skills, priority skills, roadmap. Mentors can use this to guide mentees. |
| **Gap Analysis Dashboard** | ✅ Met | Analysis page shows: match score, radar chart, matching skills (green tags), missing skills (red tags), AI insights, priority skills, recommended courses. Compare user vs 12 job roles. |
| **Dynamic Learning Roadmap** | ✅ Met | Learning roadmap: ordered steps with skill, reason, estimated weeks, difficulty. Course recommendations mapped to missing skills, sorted by rating. RoadmapPage with timeline. |
| **100+ Job Descriptions** | ⚠️ Partial | Example said "100+ job descriptions"; project has 12 job roles. Sufficient for demo; noted as limitation. |
| **Success: Clarity of Path** | ✅ Met | User gets: match %, priority skills, step-by-step roadmap with time estimates, and course links. Clear next step. |
| **Success: Data Integration** | ✅ Met | Resume parsing: paste or select 8 sample resumes. Skill extraction from resume text (FallbackService). AI extracts additional skills. |
| **Success: AI with Fallback** | ✅ Met | AI mode (Groq) for rich analysis; fallback (rule-based) when unavailable. ModeToggle in UI. |

### Step 3: Submission Deliverables

| Deliverable | Status | Location / Notes |
|-------------|--------|-------------------|
| Working Prototype | ✅ | React frontend + FastAPI backend. Run backend: `uvicorn app.main:app --reload --port 8000`. Run frontend: `npm start`. |
| Synthetic Dataset | ✅ | `backend/data/resumes.json`, `job_roles.json`, `courses.json` |
| Design Documentation | ✅ | See Design Documentation section above. |
| Completed README | ✅ | AI Disclosure and Tradeoffs sections completed below. |
| 5–7 Minute Video | 📎 | Youtube Link: https://youtu.be/duXLdD4yfc4 |

---

## Features Planned for the future

These features were skipped due to time constraints:

1. **Mock Interview Pivot** — AI-generated technical interview questions from profile skills.
2. **100+ Job Roles** — We have 12 roles. Scenario example mentioned 100+. Enough for demo.
3. **GitHub Profile Integration** — App only supports resume paste + manual skills. No GitHub API to auto-extract skills from repos.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9–3.12 (3.13 may cause pydantic install issues; use 3.11 or 3.12 if so)
- Node.js 18+
- Groq API key (free at https://console.groq.com)

### Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate.bat   # Windows
# source venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
copy .env.example .env # Windows
# cp .env.example .env # macOS/Linux
# Add your GROQ_API_KEY to .env
uvicorn app.main:app --reload --port 8000
# Note: Use "app.main:app" (not "main:app") — the app lives in app/main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The app will open at http://localhost:3000. The backend runs at http://localhost:8000.

---

## Features

- **AI-Powered Analysis** — Uses Groq API with Llama 3 for intelligent skill gap analysis
- **Smart Fallback** — Rule-based analysis works when AI is unavailable
- **12 Job Roles** — Cloud Engineer, DevOps, Full-Stack, Data Engineer, and more
- **25+ Courses** — Curated from Coursera, Udemy, freeCodeCamp, and other platforms
- **Personalized Roadmap** — Step-by-step learning path with time estimates and prerequisites

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/profiles` | GET, POST | List/Create profiles |
| `/api/profiles/{id}` | GET, PUT, DELETE | Get/Update/Delete profile |
| `/api/analysis/analyze` | POST | Run skill gap analysis |
| `/api/analysis/sample/{resume_id}/{role_id}` | GET | Quick demo analysis |
| `/api/roles` | GET | List job roles (with filters) |
| `/api/roles/{id}` | GET | Get single role |
| `/api/courses` | GET | List courses (with filters) |
| `/api/courses/recommend?skills=` | GET | Get course recommendations |
| `/api/data/resumes` | GET | Get sample resumes |

---

## Running Tests

```bash
cd backend
pytest
```

---

## Case Challenge Scoring Pillars

| Pillar | How This Project Addresses It |
|--------|-------------------------------|
| **Problem Understanding** | Clear problem: skills gap between academics and job requirements. Solution: gap analysis + learning roadmap. Scenario 2 alignment documented above. |
| **Technical Rigor** | FastAPI + React, Groq (Llama 3) for AI, rule-based fallback, Pydantic validation, pytest tests. Architecture and data model fully documented in Design Documentation section. |
| **Creativity** | Mode toggle (AI vs Manual), radar chart, timeline roadmap, prerequisite-aware roadmap ordering, sample resumes for quick demo. |
| **Prototype Quality** | Working full-stack demo: create profile → analyze → view roadmap. Core flow is functional end-to-end. |
| **Responsible AI** | Fallback is a first-class path, not an error state. No reliance on AI for critical functionality. Synthetic data only. AI mode surfaced transparently to user via `analysis_mode` field. |

---

## Video (5–7 Minute Screen Recording)

**Required deliverable.** Upload to YouTube or Vimeo (Public). Add link below.

**Video link:** https://youtu.be/duXLdD4yfc4

---

## AI Disclosure

- **Did you use an AI assistant (Copilot, ChatGPT, etc.)?** Yes.
- **How did you verify the suggestions?** Ran the code locally, ran tests, and tried the flows in the browser. For Groq, I checked the example in their docs and matched the request format. When something broke, I fixed it manually.
- **Give one example of a suggestion you rejected or changed:** An initial suggestion used substring matching in `normalize_skill()` (e.g., `"python" in "python programming"` → `"Python"`). This was rejected because `"java"` could incorrectly match inside `"javascript"`. The implementation was changed to use only exact alias matching to avoid false positives.

---

## Tradeoffs & Prioritization

- **What did you cut to stay within the 4–6 hour limit?**
  - **Mock Interview Pivot** — Not built. Would generate interview questions from skills.
  - **GitHub profile integration** — Not built. Would parse GitHub repos and infer skills. App only supports resume paste + manual skills.
  - **100+ job roles** — Built 12. Enough for demo.
  - **User auth + database** — Not built. Profiles are in-memory only.
  - **Production deploy** — Not built.

- **What would you build next if you had more time?**
  - GitHub API integration to parse repos and extract skills from code/languages
  - Mock Interview feature: AI generates role-specific technical questions from profile skills
  - Expand to 50–100 job roles with broader industries
  - Persistent storage (PostgreSQL/SQLite) and auth for saving profiles
  - Dark/light theme toggle and improved mobile responsiveness

- **Known limitations:**
  - 12 job roles (vs. scenario example of 100+); sufficient for demo
  - Profiles stored in-memory; lost on server restart
  - No authentication; anyone can create/delete profiles
  - Groq API rate limits apply; fallback mode avoids dependency

---

## License

MIT
