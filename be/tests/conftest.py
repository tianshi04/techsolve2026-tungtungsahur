import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_child_info():
    """Returns a factory for valid child info dict."""

    def _create(**kwargs):
        default = {
            "name": "Minh",
            "age": 10,
            "gender": "nam",
            "location": "TP.HCM",
            "notes": "hay chơi game online",
        }
        default.update(kwargs)
        return default

    return _create


@pytest.fixture
def sample_generate_config():
    """Returns a factory for valid generate config dict."""

    def _create(**kwargs):
        default = {"total": 2, "difficulty": 3}
        default.update(kwargs)
        return default

    return _create


@pytest.fixture
def valid_request(sample_child_info, sample_generate_config):
    """Returns a factory for valid generate request dict."""

    def _create(child_kwargs=None, config_kwargs=None):
        return {
            "child": sample_child_info(**(child_kwargs or {})),
            "config": sample_generate_config(**(config_kwargs or {})),
        }

    return _create
