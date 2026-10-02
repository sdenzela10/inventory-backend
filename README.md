# Inventory Backend

A production-oriented inventory management backend built with **FastAPI, SQLAlchemy 2.0, PostgreSQL, and Alembic**.

The application provides authentication, user-owned inventory management, stock operations, dashboard summaries, CSRF protection, CORS configuration, centralized error handling, logging, and Docker-based development.

---

## Features

* JWT authentication stored in HttpOnly cookies
* Password hashing with Passlib / bcrypt
* User authentication and current-user resolution
* User-owned inventory with strict data isolation
* Inventory CRUD operations
* Per-user SKU and item-name uniqueness
* Inventory filtering and pagination
* Stock-in and stock-out operations
* Prevention of negative stock
* User-scoped dashboard summaries
* CSRF protection using the double-submit cookie pattern
* Environment-driven CORS and cookie configuration
* Centralized application error handling
* Structured application logging
* Docker Compose development environment
* Gunicorn with Uvicorn workers

---

## Learning Goals

This project was built to develop practical experience with:

* Designing a layered backend architecture
* Building REST APIs with FastAPI
* Implementing authentication and authorization
* Working with JWTs and secure cookies
* Applying CSRF and CORS protection
* Designing database models and relationships with SQLAlchemy
* Managing schema changes with Alembic
* Separating repositories, services, dependencies, and routers
* Handling database transactions and integrity errors
* Implementing user-level data isolation
* Containerizing applications with Docker
* Running FastAPI with Gunicorn and Uvicorn
* Implementing centralized error handling and application logging

---

## Architecture

The backend follows a layered architecture:

```text
Client
  ↓
Router
  ↓
Dependencies / Schemas
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

### Responsibilities

* **Routers** — HTTP and API concerns
* **Dependencies** — authentication, CSRF, and service injection
* **Services** — business logic
* **Repositories** — database access
* **Models** — SQLAlchemy database models
* **Schemas** — Pydantic request/response validation
* **Core** — configuration, security, CSRF, and logging
* **Exceptions** — application-specific errors and handlers

---

## Project Structure

```text
inventory-backend/
├── .venv/
├── alembic/
├── app/
     ├── core/
          ├── __init__.py
          ├── config.py
          ├── csrf.py
          ├── logging.py
          ├── security.py
     ├── db/
          ├── __init__.py
          ├── base.py
          ├── database.py
     ├── dependencies/
          ├── __init__.py
          ├── auth_dependency.py
          ├── csrf_dependency.py
          ├── service_dependency.py
     ├── exceptions/
          ├── __init__.py
          ├── auth_exception.py
          ├── csrf_exception.py
          ├── exception_handlers.py
          ├── inventory_exception.py
     ├── models/
          ├── __init__.py
          ├── inventory_model.py
          ├── user_model.py
     ├── repositories/
          ├── __init__.py
          ├── inventory_repository.py
          ├── user_repository.py
     ├── routers/
          ├── __init__.py
          ├── auth_router.py
          ├── health_router.py
          ├── inventory_router.py
     ├── schemas/
          ├── __init__.py
          ├── auth_schema.py
          ├── error_schema.py
          ├── inventory_schema.py
     ├── services/
          ├── __init__.py
          ├── auth_service.py
          ├── inventory_service.py
     ├── __init__.py
     ├── main.py
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── requirements.txt
```

---

## Technology Stack

| Area                | Technology                   |
| ------------------- | ---------------------------- |
| Language            | Python                       |
| Web Framework       | FastAPI                      |
| Application Server  | Gunicorn + Uvicorn workers   |
| Containerization    | Docker + Docker Compose      |
| Database            | PostgreSQL                   |
| Production Database | Render PostgreSQL            |
| ORM                 | SQLAlchemy 2.0               |
| Migrations          | Alembic                      |
| Authentication      | JWT (`python-jose`)          |
| Password Hashing    | Passlib / bcrypt             |
| CSRF                | Double-submit cookie pattern |
| Configuration       | Pydantic Settings            |

---

## Authentication

Authentication uses JWTs stored in **HttpOnly cookies**.

The authentication flow validates registration data, hashes passwords before persistence, verifies credentials during login, creates JWTs, and resolves the authenticated user through a reusable dependency.

Passwords and password hashes are never exposed through API responses.

---

## Inventory API

All inventory endpoints require authentication.

| Method | Endpoint                     | Purpose               |
| ------ | ---------------------------- | --------------------- |
| POST   | `/inventory`                 | Create inventory item |
| GET    | `/inventory`                 | List and filter items |
| GET    | `/inventory/{item_id}`       | Get item              |
| PUT    | `/inventory/{item_id}`       | Update item           |
| DELETE | `/inventory/{item_id}`       | Delete item           |
| PATCH  | `/inventory/{item_id}/stock` | Stock-in / stock-out  |
| GET    | `/dashboard/summary`         | Inventory summary     |

Inventory records are scoped to the authenticated user.

The inventory API supports filtering, name search, price and quantity filtering, pagination, stock adjustments, and dashboard summaries.

---

## Database

PostgreSQL is used as the primary database.

* PostgreSQL through Docker Compose for local development
* Render PostgreSQL for production
* SQLAlchemy 2.0 for database access
* Alembic for database migrations

Main tables:

```text
users
inventory_items
alembic_version
```

Inventory ownership is enforced through `user_id`, with per-user uniqueness for SKU and item name.

---

## Security

### CSRF Protection

Authenticated state-changing requests require a valid CSRF token using the **double-submit cookie pattern**.

The CSRF token is provided through both a cookie and request header and is validated before protected state-changing operations.

### CORS

CORS is configured through environment settings with credentials enabled and origins restricted to the configured frontend domain.

### Cookies

Authentication and CSRF cookie behavior is environment-driven, including:

* Secure
* HttpOnly
* SameSite
* Cookie names

---

## Configuration

Configuration is managed through **Pydantic Settings**.

* `.env` — local configuration
* `.env.example` — configuration template
* Production configuration is supplied through the hosting environment

Secrets are not hardcoded in the application source.

---

## API Documentation

The application provides:

* **Swagger UI** — `/docs`
* **ReDoc** — `/redoc`
* **Health Check** — `/health`

The health endpoint returns:

```json
{"status": "ok"}
```

---

## Runtime and Error Handling

The application runs with **Gunicorn and Uvicorn workers** and is containerized for local development using Docker Compose.

Application-specific exceptions are handled centrally and return controlled API responses. Unexpected errors are handled generically without exposing internal implementation or security details.

Application logging provides operational information while avoiding sensitive authentication data such as passwords, password hashes, tokens, and cookies.

---

## Future Improvements

Potential future improvements include:

* Automated unit and integration test suites
* CI/CD pipeline
* Production deployment configuration
* API rate limiting
* Refresh token rotation
* Automated API documentation enhancements
* Monitoring and application metrics
* More advanced inventory reporting
* Frontend client integration

---

## License

Add the project's license information here if and when a license is selected.