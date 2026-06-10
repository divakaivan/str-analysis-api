import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.main import create_app  # noqa: E402


@pytest.fixture(scope="function")
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client
