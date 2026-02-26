import pytest


@pytest.fixture()
def api_client():
    """Return a Django test client for API requests."""
    from django.test import Client

    return Client()
