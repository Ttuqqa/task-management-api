import os
import tempfile

fd, path = tempfile.mkstemp(suffix=".db")
os.close(fd)

os.environ["DB_PATH"] = path
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-only-1234567890"
import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client