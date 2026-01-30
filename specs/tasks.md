# Task Breakdown: Vehicle Inventory API

According to the SDD methodology, these tasks must be executed following the RED-GREEN-VERIFY (TDD) cycle.

| Task ID | Description | Dependencies | Acceptance Criteria | Files Affected | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T001** | Docker configuration and base environment setup. | None | `docker-compose up` starts FastAPI and MongoDB without errors. | `Dockerfile`, `docker-compose.yml`, `requirements.txt` | `TODO` |
| **T002** | Database Connection and Pydantic Schemas. | T001 | Successful validation of a Vehicle object with Mexican license plate regex. | `src/database.py`, `src/schemas/vehicle.py` | `TODO` |
| **T003** | Implement Health Endpoint (`/health`). | T002 | Returns HTTP 200 and DB connection status. | `src/main.py`, `src/routes/health.py` | `TODO` |
| **T004** | Implement `POST /api/v1/vehicles` (Create). | T002 | Vehicle is saved in MongoDB and returns the created object with its ID. | `src/routes/vehicles.py`, `src/models/vehicle_dao.py` | `TODO` |
| **T005** | Implement `GET /api/v1/vehicles` with Pagination. | T004 | Returns list of vehicles; supports `limit` and `offset` parameters. | `src/routes/vehicles.py` | `TODO` |
| **T006** | Implement `GET /api/v1/vehicles/{id}` (Read). | T004 | Returns details of a specific vehicle or 404 if not found. | `src/routes/vehicles.py` | `TODO` |
| **T007** | Implement `PUT /api/v1/vehicles/{id}` (Update). | T006 | Allows modifying fields (e.g., `estado_vehiculo`) and validates data types. | `src/routes/vehicles.py` | `TODO` |
| **T008** | Implement `DELETE /api/v1/vehicles/{id}` (Delete). | T006 | Vehicle is removed from MongoDB and returns confirmation. | `src/routes/vehicles.py` | `TODO` |
| **T009** | Coverage Tests and Final Documentation. | T003 - T008 | Test coverage ≥90% and README updated. | `tests/`, `README.md`, `prompts-log.md` | `TODO` |
