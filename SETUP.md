# Quickstart & Setup Guide

Direct, copy-paste commands to set up the virtual environment, install dependencies, spin up databases, and run the server.

---

## ⚡ 1-Command Complete Setup (Docker)

Just run this single command. It builds the container, sets up the environment, verifies dependencies, runs migrations, and starts the server with hot-reload:

```bash
docker compose up
```

*(Or to run in the background: `docker compose up -d`)*

---

## 1. Setup Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 2. Upgrade Pip & Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Configure Environment

```bash
cp .env.example .env
```

---

## 4. (Optional) Start Local Databases if not using Cloud
> Since `.env` is already configured with Neon PostgreSQL and Upstash Redis, you can skip this step!
If you ever want local offline instances:
```bash
docker compose up -d postgres redis
```

---

## 5. Run the FastAPI Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 6. Verify Running Application

- **Root API**: [http://localhost:8000/](http://localhost:8000/)
- **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 7. Stop Database Containers

When you are done developing:

```bash
docker compose down
```
