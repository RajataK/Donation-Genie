import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_returns_200_when_healthy(api_client: Client):
    response = api_client.get("/api/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.django_db
def test_health_response_contains_required_fields(api_client: Client):
    response = api_client.get("/api/health/")
    data = response.json()
    required_fields = {"status", "database", "version", "timestamp"}
    assert required_fields.issubset(data.keys())


def test_health_returns_503_when_db_unreachable(api_client: Client, settings):
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "nonexistent",
            "HOST": "localhost",
            "PORT": "9999",
        }
    }
    response = api_client.get("/api/health/")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["database"] == "disconnected"
