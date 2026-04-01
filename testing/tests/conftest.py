"""Pytest configuration"""
import pytest
import os

@pytest.fixture(scope="session")
def setup_test_env():
    """Setup test environment"""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    yield
    # Cleanup
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture(autouse=True)
def clear_db():
    """Clear database before each test"""
    yield

def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test"
    )
