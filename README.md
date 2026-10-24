# Task Management API

A RESTful backend API for managing personal tasks, built with **Flask** and **SQLite**. Each user registers, logs in, and manages their own tasks. Users can never see or modify each other's data.

**Live demo:** [task-management-api-1sxp.onrender.com](https://task-management-api-1sxp.onrender.com/)

## Features

- User registration and login with **JWT authentication** (passwords are hashed, never stored in plain text)
- Full **CRUD** for tasks, scoped per user
- **Filtering** by status and priority, **search** by title, and **pagination**
- Input **validation** with clear error messages
- Consistent JSON responses with **correct HTTP status codes**
- Global **error handling** and **logging** (failed login attempts are logged)
- Automated tests with **pytest**, running on an isolated temporary database

## Tech Stack

Python 3 · Flask · SQLite · PyJWT · Werkzeug · pytest · gunicorn

## Project Structure

```
task-managment-api/
├── app.py                 # Entry point: creates the app, registers blueprints
├── config.py              # Single source of truth for settings (reads .env)
├── routes/                # HTTP layer: receives requests, returns responses
│   ├── user_routes.py
│   └── task_routes.py
├── services/              # Business logic
│   ├── user_service.py
│   └── task_service.py
├── database/
│   └── db.py              # The only layer that talks to SQL
├── utils/
│   ├── auth.py            # JWT decorator (token_required)
│   ├── validation.py      # Input validation
│   ├── response.py        # Standard success/error response format
│   ├── error_handler.py   # Global error handlers
│   └── logger.py          # Logging setup
└── tests/                 # pytest tests
```

**Request flow:** `Route → Validation → Service → Database → Response`

Each layer has one job. Routes never contain SQL, and the database layer never makes decisions about users or permissions.

## Getting Started

### 1. Clone and install

```bash
git clone <your-repo-url>
cd task-managment-api
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```
SECRET_KEY=your-long-random-secret
```

Generate a strong key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

The app refuses to start if `SECRET_KEY` is missing (fail fast), instead of failing later on the first login.

### 3. Run

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`.

### 4. Run the tests

```bash
python -m pytest
```

Tests use a temporary database, so your real data is never touched.

## API Reference

All task endpoints require the header:

```
Authorization: Bearer <token>
```

### Authentication

| Method | Endpoint    | Description                  |
|--------|-------------|------------------------------|
| POST   | `/register` | Create an account            |
| POST   | `/login`    | Log in and receive a JWT     |

Example body for both:

```json
{ "username": "sara", "password": "123456" }
```

### Tasks

| Method | Endpoint       | Description                                   |
|--------|----------------|-----------------------------------------------|
| POST   | `/tasks`       | Create a task                                 |
| GET    | `/tasks`       | List your tasks (supports filters, see below) |
| GET    | `/tasks/<id>`  | Get one task                                  |
| PUT    | `/tasks/<id>`  | Replace all task fields                       |
| PATCH  | `/tasks/<id>`  | Update only the fields you send               |
| DELETE | `/tasks/<id>`  | Delete a task                                 |

Example body for creating a task:

```json
{
  "title": "Prepare report",
  "description": "Q4 numbers",
  "priority": "High",
  "status": "Pending",
  "due_date": "2026-12-01"
}
```

**Rules**

- `title` and `due_date` are required.
- `priority` must be `High`, `Medium`, or `Low` (defaults to `Medium`).
- `status` must be `Pending`, `In Progress`, or `Done` (defaults to `Pending`).
- Passwords must be at least 6 characters.

### Filtering, search, and pagination

`GET /tasks` accepts optional query parameters that can be combined:

| Parameter  | Example                  | Meaning                                  |
|------------|--------------------------|------------------------------------------|
| `status`   | `?status=Done`           | Only tasks with this status              |
| `priority` | `?priority=High`         | Only tasks with this priority            |
| `search`   | `?search=report`         | Title contains the text                  |
| `page`     | `?page=2`                | Page number (default 1)                  |
| `limit`    | `?limit=10`              | Tasks per page (default 10, max 50)      |

Example: `GET /tasks?status=Done&priority=Low&page=1&limit=5`

### Response format

Every response uses the same shape:

```json
{
  "success": true,
  "message": "Tasks retrieved successfully",
  "data": []
}
```

### Status codes

| Code | When                                                          |
|------|---------------------------------------------------------------|
| 200  | Request succeeded                                             |
| 201  | Resource created (new task)                                   |
| 400  | Invalid or missing input (validation failed)                  |
| 401  | Missing/invalid token, or wrong username or password          |
| 404  | Task not found (or it belongs to another user), unknown route |
| 409  | Username already exists                                       |
| 500  | Unexpected server error                                       |

## Design Decisions

**Why 404 instead of 403 when accessing another user's task?**
Returning `403 Forbidden` would confirm that task #42 exists and belongs to someone else. An attacker could loop over IDs and map which ones exist (resource enumeration). Every task query filters by both `id` and `user_id`, so another user's task is indistinguishable from one that doesn't exist, and the API answers `404` in both cases.

**Why the same `401` and message for a wrong username and a wrong password?**
Different responses would reveal which usernames are registered (user enumeration). Both cases return the identical response.

**Why `PATCH` for partial updates?**
`PUT` replaces the whole resource, so omitted fields would be lost. `PATCH` keeps existing values for any field not sent.

**Why a separate `config.py`?**
Settings are read in one place, so no module depends on import order to see them. This fixed a real bug during development, where `SECRET_KEY` was read before `.env` was loaded and login crashed.

**Why parameterized SQL queries?**
All values are passed as parameters (`?`), never concatenated into the query string, which prevents SQL injection, including in the dynamic filter and search query.

## Known Limitations and Next Steps

- `due_date` is stored as text and its format is not validated yet.
- SQLite is used for simplicity. A production deployment would move to PostgreSQL with migrations.
- No refresh tokens: tokens expire after 1 hour and the user must log in again.
- On free hosting tiers with an ephemeral filesystem, the SQLite file can be reset on redeploy.

