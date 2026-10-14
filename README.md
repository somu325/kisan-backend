# Kisan Backend

Production-grade asynchronous FastAPI backend engineered with **PostgreSQL**, **Redis**, **SQLAlchemy 2.0 (asyncpg)**, and **Alembic**, modularly structured for external API integrations, web scraping, and LLM-powered report pipelines.

---

## 🏗️ Architecture & Project Structure

```text
kisan-backend/
├── app/
│   ├── api/                     # API Layer
│   │   ├── deps.py              # Annotated Dependency Injection (DB, Redis, etc.)
│   │   └── v1/
│   │       ├── api.py           # V1 Router Aggregator
│   │       └── endpoints/       # Endpoint definitions
│   │           ├── health.py    # PG & Redis connectivity health check
│   │           ├── reports.py   # Reports router placeholder
│   │           └── scrapers.py  # Scrapers router placeholder
│   ├── core/                    # Core Infrastructure
│   │   ├── config.py            # Pydantic v2 BaseSettings
│   │   ├── database.py          # Async SQLAlchemy engine & session maker
│   │   ├── redis.py             # Async Redis connection pool & lifecycle
│   │   ├── logging.py           # Structured logging
│   │   └── exceptions.py        # Global exception handling
│   ├── models/                  # SQLAlchemy ORM models
│   │   └── base.py              # Base model with auto tablenames & timestamps
│   ├── schemas/                 # Pydantic v2 schemas
│   │   └── common.py            # Standardized API response models
│   ├── services/                # Business logic layer
│   │   ├── external/            # HTTPX Async clients for external APIs
│   │   ├── scraper/             # Web scraping engine
│   │   ├── llm/                 # LLM prompts & client integrations
│   │   └── reports/             # Report generators
│   ├── utils/                   # Helpers and utility functions
│   └── main.py                  # FastAPI app factory, CORS, and Lifespan
├── alembic/                     # Alembic database migrations
│   ├── env.py
│   └── versions/
├── tests/                       # Async pytest suite
│   ├── conftest.py
│   └── test_health.py
├── .env.example                 # Environment variables template
├── .env                         # Local environment configuration
├── .dockerignore
├── .gitignore
├── alembic.ini                  # Migration settings
├── Dockerfile                   # Multi-stage production Docker container
├── docker-compose.yml           # Docker Compose with FastAPI, Postgres & Redis
├── pyproject.toml               # Project metadata & tool config (ruff, pytest)
└── requirements.txt             # Direct dependencies
```

---

## 🚀 Quickstart with Docker (Recommended)

To start the full stack (**FastAPI**, **PostgreSQL**, **Redis**) with hot-reload and volume persistence:

```bash
# 1. Build and start containers in the background
docker compose up --build -d

# 2. View logs in real-time
docker compose logs -f api

# 3. Check container status and health
docker compose ps
```

Once running:
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check Endpoint**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

To stop services:
```bash
docker compose down
```

---

## 💻 Manual Local Setup

If you prefer running directly on your host machine:

### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start Database & Redis (via Docker)
If PostgreSQL and Redis are not installed locally on your machine, launch just the database services:
```bash
docker compose up -d postgres redis
```

### 4. Run Migrations (Optional / When models are added)
```bash
# Generate a new migration
alembic revision --autogenerate -m "initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Launch FastAPI Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Running Tests & Linting

```bash
# Run tests
pytest

# Run linter
ruff check .

# Auto-fix linting issues
ruff check --fix .
```
