# Fleet Management API

API for managing the vehicle fleet inventory. Built with FastAPI and MongoDB.

## Tech Stack
- **Python** 3.11+
- **FastAPI**
- **MongoDB**
- **Docker** (for Database)

## Setup

### Prerequisites
1.  Python 3.11+ installed.
2.  Docker and Docker Compose installed.

### Installation

1.  **Clone the repository** (or navigate to project root).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start Database**:
    ```bash
    docker-compose up -d
    ```
    This starts a MongoDB instance on `localhost:27017`.

4.  **Run the Application**:
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at [http://localhost:8000](http://localhost:8000).

## API Documentation

Interactive documentation is available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing

Run the test suite with coverage:
```bash
pytest --cov=src tests/
```
