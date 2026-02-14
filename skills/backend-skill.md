Backend Development Standards
Architecture & Organization

    Flat Path Policy: Always use flat URL structures (e.g., /api/v1/assignments?driver_id={id}).

    NEVER use nested resource paths like /drivers/{d_id}/vehicles/{v_id}.

    Repository Pattern: Abstract all PyMongo logic into dedicated repository classes to keep route handlers clean.

    Atomization: Functions must perform a single task. NEVER exceed 40 lines of logic per function.

API Design & HTTP Methods

    Strict REST: Use POST for creation, GET for retrieval, PUT/PATCH for updates, and DELETE for removal.

    Parameter Identification: Pass unique identifiers via query parameters or simple path variables, avoiding complex hierarchies.

Data Validation (Pydantic)

    Strict Modeling: Implement separate models for Create, Update, and Response schemas.

    Validation Rules: Use Extra.forbid in Pydantic configurations to reject any unexpected fields in the request body.

Error Handling

    Custom Exceptions: Catch low-level database or system errors and raise domain-specific exceptions (e.g., DriverNotFoundError).

    User-Friendly Responses: Ensure all raised exceptions return a structured JSON response with a clear message and appropriate HTTP status code (e.g., 404 for missing resources).

    NEVER expose raw Python tracebacks or MongoDB error strings to the client.

Database Access (PyMongo)

    Injection Prevention: Use parameterized queries provided by PyMongo. NEVER use f-strings to build query filters.

    Connection Management: Use FastAPI dependencies to manage the lifecycle of the MongoDB client.

Security & Clean Code

    Credential Safety: Use .env files for all secrets. NEVER hardcode API keys or DB URIs.

    Side-Effect Isolation: Separate data transformation logic from database I/O functions.