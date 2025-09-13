# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install -e .[dev]

COPY app /app/app
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# Non-root user (optional but recommended)
RUN useradd -u 10001 -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]