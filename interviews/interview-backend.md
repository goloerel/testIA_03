1. interview-backend.md

Role: Backend Developer (FastAPI + MongoDB)

Goal: Extracting tacit knowledge for Fleet Management API.

Interviewer: How do you structure API endpoints and handle HTTP methods?

User: I prefer a flat structure using parameters for IDs rather than nested paths. I want to enforce the use of correct HTTP methods for this practice.

Interviewer: What is your preference for Pydantic validation?

User: I prefer the "Strict" option. We should use separate models for different actions (Create, Update, Response) to ensure data integrity.

Interviewer: How should we handle exceptions?

User: I prefer to catch exceptions and raise custom ones to allow for better error management and user-friendly messages.

Interviewer: What are your thoughts on database patterns and code organization?

User: We use MongoDB and prefer atomized, well-designed functions for reusability. We should avoid global objects and keep logic modular.

Interviewer: Any specific "Never" rules for security or style?

User: NEVER hardcode credentials. NEVER use long, "God-object" functions; they must be small and easy to identify.