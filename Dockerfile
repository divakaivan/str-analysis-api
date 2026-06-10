FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

COPY . /app
WORKDIR /app
ENV UV_NO_DEV=1
RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
