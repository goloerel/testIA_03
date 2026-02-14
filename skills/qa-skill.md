Testing Standards
Test Structure & Naming

    Naming Pattern: Use the format test_[action]_[expected_result]. (e.g., test_get_driver_not_found).

    Philosophy: Prioritize readability so that anyone can recognize exactly what is being tested at a glance. 

Environment & Integration

    Database Strategy: Always run tests against a real MongoDB instance inside a Docker container.

    Isolation: NEVER use mongomock unless explicitly required for unit-level logic that doesn't touch the DB. 

E2E Testing

    Flows: Ensure key admin flows (Create, Update, Delete) are covered using Playwright.

    Clean State: NEVER leave leftover data in the database between test runs; ensure a clean "Given" state.