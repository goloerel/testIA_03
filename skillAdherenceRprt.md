Deliverable 11: Skill Adherence Report Template

This report calculates your final Skill Adherence Score, which contributes 25 points to your total grade.
1. Backend Adherence (FastAPI + MongoDB)

    [ ] Flat Structure: All API endpoints use parameters and avoid nested paths (e.g., /api/v1/assignments?driver_id=...).

    [ ] Strict Pydantic: Separate models exist for Create, Update, and Response with Extra.forbid enabled.

    [ ] Custom Exceptions: Global exception handlers catch domain errors and return user-friendly messages.

    [ ] Atomized Functions: No single function exceeds the 40-line logic limit.

    [ ] Repository Pattern: MongoDB queries are isolated from route handlers.

2. Frontend Adherence (Vanilla HTML/CSS/JS)

    [ ] CSS Naming: All classes use single hyphens - only (no underscores or double-symbols).

    [ ] File Structure: Main styles are consolidated in main.css.

    [ ] Data Flow: State and data are passed explicitly between functions, not stored in a global object.

    [ ] No Frameworks: Project is built with 100% pure HTML, CSS, and JS.

3. QA Adherence (Pytest + Playwright)

    [ ] Naming Convention: Test functions follow the test_[action]_[expected_result] pattern.

    [ ] Integration Environment: Tests run against a live MongoDB Docker container.

    [ ] Coverage: Backend coverage meets the minimum 80% threshold.