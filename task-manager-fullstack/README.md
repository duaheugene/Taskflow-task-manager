# Taskflow — Full-stack CRUD Task Manager

A responsive full-stack task manager built for the CRUD Task Manager assignment. It includes a browser-based frontend, a REST API, SQLite persistence, registration/login, password hashing, JWT authentication, and per-user task ownership.

## Features

- Register and sign in with email and password.
- Passwords are hashed with Argon2; plain-text passwords are never stored.
- JWT-protected API routes.
- Create, list, view, update, and delete tasks (CRUD).
- Task title, description, status, priority, and optional due date.
- Filter by status, search titles/descriptions in the UI, and sort tasks.
- Dashboard statistics and completion progress.
- User isolation: each user can only access their own tasks.
- Responsive UI with empty states, validation messages, and notifications.
- Interactive API documentation at `/docs`.

## Technology stack

- **Python 3.10+**
- **FastAPI** — REST API and application server
- **SQLAlchemy 2** — database ORM
- **SQLite** — local relational database (created automatically)
- **Pydantic** — request validation and response schemas
- **Argon2 via argon2-cffi** — password hashing
- **PyJWT** — signed access tokens
- **HTML, CSS, JavaScript** — frontend, served by FastAPI
- **Uvicorn** — local ASGI server
- **pytest + HTTPX** — automated testing dependencies

## Requirements

Install Python 3.10 or newer. You do not need to install SQLite separately for the default local setup.

## Setup and run (Windows PowerShell)

1. Extract the project folder and open it in VS Code.
2. Open Terminal → New Terminal and move into the folder containing `README.md`.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

4. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or temporarily permit activation in your current PowerShell session with `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. (Recommended before deployment) Copy `.env.example` to `.env`, choose a long random `SECRET_KEY`, and configure environment variables. The app reads environment variables from the process; it does not automatically load `.env`. In PowerShell for a local run, you can set one directly:

   ```powershell
   $env:SECRET_KEY = "replace-with-a-long-random-secret"
   ```

7. Start the server from the project root:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

8. Open **http://127.0.0.1:8000** in your browser. Register an account, then create tasks.
9. Open **http://127.0.0.1:8000/docs** to explore and test the API.

The `task_manager.db` database file is created automatically in the working directory on first startup.

## Setup and run (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export SECRET_KEY="replace-with-a-long-random-secret"
python -m uvicorn app.main:app --reload
```

Then visit `http://127.0.0.1:8000`.

## API reference

All task endpoints require `Authorization: Bearer <access_token>`. Register and login return the token. In Swagger UI, click **Authorize** and enter the token as `Bearer <token>` if prompted by the HTTP bearer scheme.

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| `POST` | `/api/auth/register` | Create account and receive token | No |
| `POST` | `/api/auth/login` | Sign in and receive token | No |
| `GET` | `/api/auth/me` | Current account details | Yes |
| `GET` | `/api/tasks` | List own tasks; optional `status` and `search` query parameters | Yes |
| `POST` | `/api/tasks` | Create a task | Yes |
| `GET` | `/api/tasks/{task_id}` | Read one own task | Yes |
| `PATCH` | `/api/tasks/{task_id}` | Update selected fields | Yes |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task | Yes |
| `GET` | `/health` | Health check | No |

### Example request bodies

Register:

```json
{
  "name": "Eugene Duah",
  "email": "eugene@example.com",
  "password": "a-strong-password"
}
```

Create task:

```json
{
  "title": "Study FastAPI",
  "description": "Build and test the CRUD endpoints",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-11-01"
}
```

Allowed status values: `pending`, `in_progress`, `completed`. Allowed priority values: `low`, `medium`, `high`. `due_date` is optional and uses `YYYY-MM-DD`.

## Project structure

```text
task-manager-fullstack/
├── app/
│   ├── __init__.py
│   ├── auth.py          # JWT authentication dependency
│   ├── config.py        # Environment-based configuration
│   ├── database.py      # SQLAlchemy engine and sessions
│   ├── main.py          # FastAPI app and frontend hosting
│   ├── models.py        # User and Task database models
│   ├── routes.py        # Authentication and CRUD endpoints
│   ├── schemas.py       # Validated request/response schemas
│   ├── security.py      # Password hashing and token creation
│   └── static/
│       ├── index.html   # Frontend structure
│       ├── styles.css   # Responsive styling
│       └── app.js       # Frontend state and API requests
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Security notes

- Passwords are hashed with Argon2.
- Task routes require a valid signed token.
- Every task query includes the authenticated user's ID to prevent users from reading, editing, or deleting other users' tasks.
- Set a strong, private `SECRET_KEY` for every deployed environment. Never commit real secrets or production database credentials.
- This is a learning project. For production use, add HTTPS, rate limiting, token revocation/refresh strategy, migrations (for example Alembic), stricter operational logging, and a managed database.
- The frontend stores its access token in browser `localStorage` for this learning implementation. A production app may prefer secure, HttpOnly cookies and a suitable CSRF strategy.

## Troubleshooting

- **`python` is not recognized:** install Python and enable “Add Python to PATH”, or try `py` on Windows.
- **`ModuleNotFoundError`:** activate the project's virtual environment and run `pip install -r requirements.txt` again.
- **Port 8000 is busy:** run `python -m uvicorn app.main:app --reload --port 8001` and visit port 8001.
- **Reset local data:** stop the server and delete `task_manager.db`. This permanently removes local accounts and tasks.

## Run tests

From the project root with the virtual environment active:

```bash
pytest -q
```

## Suggested GitHub workflow

```bash
git init
git add .
git commit -m "Build full-stack CRUD task manager"
```

Create an empty GitHub repository, add it as `origin`, and push your branch. Do not commit `.env`, secrets, or the local database.
