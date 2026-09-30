import os

os.environ["DATABASE_URL"] = "sqlite:///./test_terapia.db"
os.environ["JWT_SECRET"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app
from app.seed import seed


@pytest.fixture(scope="session", autouse=True)
def database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    seed()
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def tokens(client):
    def login(email):
        response = client.post("/auth/login", data={"username": email, "password": "Demo123!"})
        assert response.status_code == 200
        return response.json()["access_token"]

    return {
        "young": login("jovem@demo.local"),
        "admin": login("admin@demo.local"),
        "research": login("pesquisa@demo.local"),
        "psychologist": login("psicologa@demo.local"),
    }


def auth(token):
    return {"Authorization": f"Bearer {token}"}
