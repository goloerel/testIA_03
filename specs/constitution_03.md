Purpose: Non-negotiable rules for security and compliance.

    Security First: Sensitive credentials must never be committed to version control; use .env files and .env.example templates.

    Data Integrity: All database interactions must use parameterized queries to prevent injection attacks.

    Availability: The API must include a /health endpoint to facilitate container orchestration and monitoring.

    Privacy: Personally Identifiable Information (PII) must be handled according to local data protection standards.