# FastAPI Task & User Management REST API 🚀

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)](https://www.sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Secure_Auth-black.svg?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A robust, production-ready RESTful API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**, featuring secure user authentication with **Argon2 password hashing**, **JWT (JSON Web Tokens)**, and full **CRUD operations** for task management.

---

## 🌟 Highlights & Features

- 🔐 **Secure Authentication**: User registration with collision handling and Argon2 password hashing via `pwdlib`.
- 🎟️ **JWT Token Generation**: Industry-standard JSON Web Token generation with configurable expiration and algorithms.
- 📋 **Complete Task CRUD**:
  - `POST /tasks` — Create new tasks with title, description, and status.
  - `GET /tasks` — Retrieve all tasks.
  - `GET /tasks/{id}` — Fetch individual task by ID with 404 validation.
  - `PUT /tasks/{id}` — Update task details and completion status.
  - `DELETE /tasks/{id}` — Delete a task and return removed payload.
- 🗄️ **Flexible Database Layer**: Powered by SQLAlchemy ORM. Seamlessly switch between **PostgreSQL** for production and **SQLite** for rapid local development.
- ⚡ **Auto-Generated Interactive Documentation**: Swagger UI (`/docs`) and ReDoc (`/redoc`) out of the box.

---

## 🏗️ Architecture & Request Flow

```mermaid
flowchart TD
    Client([Client / Frontend / Postman])
    
    subgraph FastAPI Application
        Router[API Endpoints]
        Auth[JWT & Password Hash Layer]
        Pydantic[Pydantic Validation Schemas]
        ORM[SQLAlchemy ORM Models]
    end
    
    subgraph Database
        DB[(PostgreSQL / SQLite)]
    end
    
    Client -->|/register & /login| Auth
    Auth -->|Access Token| Client
    Client -->|CRUD Requests /tasks| Router
    Router --> Pydantic
    Pydantic --> ORM
    ORM --> DB
```

---

## 📁 Project Structure

```
FASTAPI/
├── database.py         # SQLAlchemy engine, session factory, & get_db dependency
├── models.py           # Database entity declarations (Task, User)
├── schemas.py          # Pydantic request & response validation schemas
├── main.py             # FastAPI instance, route handlers, auth logic
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- Virtualenv or Conda
- PostgreSQL (optional, can use SQLite out of the box)

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/swayam690/fastapi-task-auth-service.git
cd fastapi-task-auth-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

To run with SQLite (default for development):
```bash
export DATABASE_URL="sqlite:///./tasks.db"
```

To run with PostgreSQL:
```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/taskdb"
```

### 4. Run the Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit the interactive Swagger UI at: **`http://localhost:8000/docs`**

---

## 📖 API Documentation & Endpoints

### 🔐 Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "developer",
  "password": "supersecretpassword"
}
```
*Response (`200 OK`):*
```json
{
  "id": 1,
  "username": "developer"
}
```

#### User Login
```http
POST /login
Content-Type: application/json

{
  "username": "developer",
  "password": "supersecretpassword"
}
```
*Response (`200 OK`):*
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 📋 Task Endpoints

| Method | Endpoint | Description | Request Body | Response Model |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/tasks` | Create a new task | `TaskInput` | `TaskOutput` |
| `GET` | `/tasks` | List all tasks | None | `list[TaskOutput]` |
| `GET` | `/tasks/{id}` | Get task by ID | None | `TaskOutput` |
| `PUT` | `/tasks/{id}` | Update task | `TaskInput` | `TaskOutput` |
| `DELETE` | `/tasks/{id}` | Delete task | None | `TaskInput` |

#### Create Task Example
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete System Integration",
    "description": "Finalize Docker and deployment pipeline",
    "completed": false
  }'
```

#### Get All Tasks Example
```bash
curl -X GET http://localhost:8000/tasks
```

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

