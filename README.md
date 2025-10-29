# Svelte + FastAPI Template

[![CI](https://github.com/stedonnelly/svelteapp-fastapi-template/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/stedonnelly/svelteapp-fastapi-template/actions/workflows/ci.yml)

A modern full-stack application template featuring:
- **Frontend**: SvelteKit 2 with TypeScript, Tailwind CSS 4, and Vite
- **Backend**: FastAPI with async SQLAlchemy, Alembic migrations, and cookie-based sessions
- **Database**: PostgreSQL 16
- **Development**: Docker Compose setup with hot-reload for both frontend and backend

## Features

### Backend (FastAPI)
- FastAPI with async/await support
- SQLAlchemy 2.0+ with async engine
- Alembic database migrations
- Cookie-based authentication with session management
- Pydantic v2 for data validation
- CORS middleware configured
- Health check endpoint
- Pytest setup with test coverage
- Code quality tools (Ruff, mypy, pre-commit)

### Frontend (SvelteKit)
- SvelteKit 2 with TypeScript
- Tailwind CSS 4 with forms and typography plugins
- Svelte 5 with modern reactivity
- API client with authentication store
- Login page example
- ESLint and Prettier configured

## Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- That's it! Everything else runs in containers.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/stedonnelly/svelteapp-fastapi-template.git
   cd svelteapp-fastapi-template
   ```

2. **Start the development environment**
   ```bash
   docker compose -f docker-compose.dev.yaml up
   ```

   This will:
   - Start PostgreSQL database on port `5432`
   - Start FastAPI backend on port `8000`
   - Start SvelteKit frontend on port `5173`
   - Run database migrations automatically
   - Enable hot-reload for both frontend and backend

3. **Access the application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs (Swagger UI)
   - **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)

## Environment Variables

The project uses `.env.dev` for development configuration. Key variables include:

### Database
- `POSTGRES_USER`: Database username (default: `postgres`)
- `POSTGRES_PASSWORD`: Database password (default: `postgres`)
- `POSTGRES_DB`: Database name (default: `app_db`)
- `POSTGRES_HOST`: Database host (default: `db` for Docker)

### Backend
- `SECRET_KEY`: Secret key for sessions (**change in production!**)
- `ALLOWED_ORIGINS`: CORS allowed origins
- `SECURE_COOKIES`: Set to `true` in production
- `SESSION_MAX_AGE_SECONDS`: Session duration (default: 7 days)

### Frontend
- `PUBLIC_API_BASE_URL`: Backend API URL (default: `http://localhost:8000/api/v1`)
- `PUBLIC_APP_NAME`: Application name

## Development Workflow

### Hot Reload
Both frontend and backend support hot reload:
- **Backend**: Code changes in `backend/app/` are automatically reloaded
- **Frontend**: Changes in `web/src/` trigger instant updates in the browser

### Running Database Migrations

Migrations run automatically on container startup, but you can run them manually:

```bash
# Create a new migration
docker compose -f docker-compose.dev.yaml exec backend alembic revision --autogenerate -m "Description"

# Apply migrations
docker compose -f docker-compose.dev.yaml exec backend alembic upgrade head

# Rollback one migration
docker compose -f docker-compose.dev.yaml exec backend alembic downgrade -1
```

### Running Tests

**Backend tests:**
```bash
docker compose -f docker-compose.dev.yaml exec backend pytest
```

**Frontend tests:**
```bash
docker compose -f docker-compose.dev.yaml exec web npm test
```

### Code Quality

**Backend linting and formatting:**
```bash
# Lint with Ruff
docker compose -f docker-compose.dev.yaml exec backend ruff check app/

# Format code
docker compose -f docker-compose.dev.yaml exec backend ruff format app/

# Type checking with mypy
docker compose -f docker-compose.dev.yaml exec backend mypy app/
```

**Frontend linting and formatting:**
```bash
# Lint
docker compose -f docker-compose.dev.yaml exec web npm run lint

# Format
docker compose -f docker-compose.dev.yaml exec web npm run format
```

## Project Structure

```
.
├── backend/                 # FastAPI application
│   ├── alembic/            # Database migrations
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── auth/           # Authentication logic
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database session
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── tests/          # Backend tests
│   │   └── utils/          # Utilities
│   ├── Dockerfile
│   └── pyproject.toml      # Python dependencies
│
├── web/                    # SvelteKit application
│   ├── src/
│   │   ├── lib/            # Shared components & utilities
│   │   └── routes/         # SvelteKit routes
│   ├── static/             # Static assets
│   ├── package.json        # Node dependencies
│   └── vite.config.ts
│
└── docker-compose.dev.yaml # Development environment
```

## API Endpoints

### Health
- `GET /api/v1/health/healthz` - Health check endpoint

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Users
- `GET /api/v1/users/` - List users (authenticated)
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}` - Get user by ID

## Stopping the Application

```bash
# Stop containers (keeps data)
docker compose -f docker-compose.dev.yaml down

# Stop and remove volumes (deletes database data)
docker compose -f docker-compose.dev.yaml down -v
```

## Troubleshooting

### Port Already in Use
If ports 5432, 8000, or 5173 are already in use, you can either:
1. Stop the conflicting service
2. Modify the port mappings in `docker-compose.dev.yaml`

### Database Connection Issues
Ensure the database container is healthy:
```bash
docker compose -f docker-compose.dev.yaml ps
```

### Backend Not Starting
Check backend logs:
```bash
docker compose -f docker-compose.dev.yaml logs backend
```

### Frontend Not Starting
Check if node_modules are properly installed:
```bash
docker compose -f docker-compose.dev.yaml exec web npm ci
```

## Production Deployment

**Before deploying to production:**

1. Generate a secure `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Update environment variables:
   - Set `ENV=production`
   - Set `SECURE_COOKIES=true`
   - Use strong database password
   - Update `ALLOWED_ORIGINS` to your production domain

3. Consider creating a separate `docker-compose.prod.yaml` with:
   - Production-ready server configurations
   - Proper volume management
   - SSL/TLS termination
   - Environment-specific optimizations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
