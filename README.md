# String Analysis API

A FastAPI-based service for analyzing strings with various analyzers.

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) (fast Python package installer and resolver)

## Local Development Setup

### 1. Install Dependencies with uv

```bash
uv sync
```

This command will install all project dependencies and dev dependencies specified in `pyproject.toml`.

### 2. Use uv to run commands

```bash
uv run <command>
```

## Running the Development Server

Start the FastAPI development server with hot reload:

```bash
uv run uvicorn src.main:create_app --factory --reload
```

The API will be available at `http://localhost:8000`

## Running Tests

Run all tests:

```bash
uv run pytest tests/
```

## Pre-commit Hooks

Pre-commit hooks help maintain code quality by running checks before each commit.

### Install Pre-commit Hooks

```bash
uv run pre-commit install
```

### Run Pre-commit Hooks

Run hooks on all files:

```bash
uv run pre-commit run --all-files
```

## Project Structure

```
src/
  analyzers/       # String analyzers
  main.py          # FastAPI application entry point
  routes.py        # API routes
  schemas.py       # Pydantic models
  settings.py      # Configuration
  helpers.py       # Utility functions
tests/             # Test suite
```
