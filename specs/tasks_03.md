1. Project Directory Structure

The following structure must be maintained to ensure role-specific isolation:
Plaintext

project/
├── skills/                  # YOUR SKILL FILES [cite: 195]
│   ├── backend-skill.md
│   ├── frontend-skill.md
│   └── qa-skill.md
├── interviews/              # INTERVIEW TRANSCRIPTS [cite: 195]
│   ├── interview-backend.md
│   ├── interview-frontend.md
│   └── interview-qa.md
├── specs/                   # PROJECT GOVERNANCE [cite: 195]
│   ├── constitution.md
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
├── backend/                 # API CODE (Python/FastAPI) [cite: 195]
│   ├── app/
│   │   ├── main.py
│   │   ├── models/          # Strict Pydantic models [cite: 195]
│   │   ├── routes/          # Flat URL endpoints [cite: 196]
│   │   ├── repositories/    # Atomized DB logic
│   │   └── database.py
│   ├── tests/               # Pytest suite [cite: 196]
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # ADMIN INTERFACE (Vanilla) [cite: 195]
│   ├── index.html           # Dashboard [cite: 189, 195]
│   ├── css/                 # main.css [cite: 196]
│   └── js/                  # Functional JS [cite: 196]
├── e2e/                     # E2E TESTS (Playwright) [cite: 196]
├── docker-compose.yml       # ORCHESTRATION [cite: 196]
└── skill-adherence-report.md # EVALUATION [cite: 196]

2. Immediate TODO List

    [ ] Task 0: Refactor Day 1-2 Codebase 

        Review existing Vehicles CRUD logic.

        Convert all nested paths to Flat Parameter structure.

        Split models into Strict Create/Update/Response schemas.

        Migrate inline DB calls to the Repository Pattern.

    [ ] Task 1: Infrastructure Setup 

        Build Dockerfile and docker-compose.yml with MongoDB volume persistence. 

        Verify GET /health endpoint works in container. 

    [ ] Task 2: Backend Expansion (Drivers & Assignments) 

        Implement Drivers CRUD with status transitions. 

        Implement Assignments CRUD (linking Driver IDs to Vehicle IDs). 

    [ ] Task 3: Stats API 

        Create GET /api/v1/stats for counts and summaries. 

    [ ] Task 4: Vanilla Frontend Development 

        Build Dashboard, Vehicles, Drivers, and Assignments pages using no frameworks.