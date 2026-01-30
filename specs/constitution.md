# Project Constitution: Fleet Management API

## 1. Introduction
This document establishes the ground rules, standards, and architectural principles for the development of the Fleet Management API. All contributors must adhere to these guidelines to ensure consistency, maintainability, and quality.

## 2. Technology Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: MongoDB (Local) with PyMongo driver
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest
- **Methodology**: Spec Driven Development (SDD) & Test Driven Development (TDD)

## 3. Coding Standards

### 3.1 Style Guide
- **PEP 8**: All code must follow PEP 8 style guidelines.
- **Formatter**: Use `black` for code formatting.
- **Linter**: Use `ruff` or `flake8` for linting.

### 3.2 Type Hinting
- **Strict Typing**: Python type hints are mandatory for all function arguments and return values.
- **Pydantic**: Use Pydantic models for data validation and serialization.

### 3.3 Documentation
- **Docstrings**: All modules, classes, and public functions must have docstrings.
- **Format**: Google Style Python Docstrings.
- **Comments**: Explain "why", not "what".

## 4. Architecture Principles

### 4.1 Layered Architecture
The application will follow a clean, layered architecture to ensure separation of concerns:

1.  **Presentation Layer (Routers)**: Handles HTTP requests/responses. Minimal logic.
2.  **Service Layer (Business Logic)**: Contains the core business rules and use cases.
3.  **Data Access Layer (Repositories)**: Handles interaction with MongoDB.
4.  **Domain Layer (Models/Schemas)**: Defines the data structures and entities.

### 4.2 Dependency Injection
- **DI**: Use FastAPI's dependency injection system to manage dependencies (e.g., database connections, services).

## 5. Testing Requirements

### 5.1 Test Driven Development (TDD)
- **Red-Green-Refactor**: Write tests before implementing functionality.
- **Scope**: Unit tests for services and repositories; Integration tests for API endpoints.

### 5.2 Coverage
- **Minimum Coverage**: >90% code coverage is required.
- **Tools**: `pytest-cov` for measuring coverage.

## 6. Error Handling

### 6.1 Standardization
- Use a centralized error handling mechanism (Exception Handlers).
- Return standard HTTP status codes (200, 201, 400, 404, 422, 500).
- Error responses must follow a consistent JSON structure:
  ```json
  {
    "error": "ErrorType",
    "message": "Human readable message",
    "details": { ... }
  }
  ```

### 6.2 Custom Exceptions
- Define domain-specific exceptions in the service layer to avoid leaking implementation details (e.g., `VehicleNotFoundException` instead of raw DB errors).

## 7. Version Control & Workflow

### 7.1 Commit Strategy
- **Conventional Commits**: Follow the Conventional Commits specification.
  - `feat: add vehicle creation endpoint`
  - `fix: validate license plate format`
  - `docs: update constitution`
  - `test: add tests for vehicle service`
  - `refactor: optimize database query`

### 7.2 Branching
- **Main**: Production-ready code.
- **Develop**: Integration branch.
- **Feature Branches**: `feat/feature-name`
- **Fix Branches**: `fix/issue-description`

## 8. Directory Structure
```
/
├── contracts/          # OpenAPI/Swagger specs
├── specs/              # SDD Documentation (MD files)
├── src/                # Source Code
│   ├── api/            # Routers/Controllers
│   ├── core/           # Config, Exceptions, Utils
│   ├── models/         # Domain Models (Pydantic)
│   ├── repositories/   # Database interactions
│   ├── services/       # Business Logic
│   └── main.py         # App Entrypoint
├── tests/              # Test Suite
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
