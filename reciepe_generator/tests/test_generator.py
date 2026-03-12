import os
import json
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# ensure API key exists before importing config
os.environ.setdefault("OPENAI_API_KEY", "fake-key-for-tests")

# Add parent directory to path so we can import reciepe_generator modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator import generate_meal_kit
from models import WishListInput, MealKit



class DummyMessage:
    def __init__(self, content: str):
        self.content = content


class DummyChoice:
    def __init__(self, content: str):
        self.message = DummyMessage(content)


class DummyResponse:
    def __init__(self, content: str):
        self.choices = [DummyChoice(content)]


@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    """Replace OpenAI client.chat.completions.create with a mock that returns deterministic responses."""
    sample_response = {
        "kit_name": "Test Soup",
        "impact_message": "This meal brings warmth and hope.",
        "description": "A hearty soup made from donated ingredients.",
        "difficulty_level": "Easy",
        "prep_time_minutes": 15,
        "servings": 4,
        "ingredients": [
            {"item": "canned tomatoes", "quantity": "2 cups", "is_from_wishlist": True},
        ],
        "instructions": [
            {"step_number": 1, "instruction": "Combine and simmer."}
        ],
    }
    
    def mock_create(*args, **kwargs):
        return DummyResponse(json.dumps(sample_response))
    
    # Patch the client's chat.completions.create method
    monkeypatch.setattr('generator.client.chat.completions.create', mock_create)


def test_generate_meal_kit_success():
    wish = WishListInput(items=["canned tomatoes"])
    meal_kit = generate_meal_kit(wish)

    assert isinstance(meal_kit, MealKit)
    assert meal_kit.kit_name == "Test Soup"
    assert meal_kit.prep_time_minutes == 15
    assert meal_kit.ingredients[0].item == "canned tomatoes"


def test_generate_meal_kit_api_error():
    """Test that API errors are properly caught and re-raised as RuntimeError."""
    def bad_create(*args, **kwargs):
        raise RuntimeError("service unavailable")

    with patch('generator.client.chat.completions.create', side_effect=bad_create):
        wish = WishListInput(items=["rice"])
        with pytest.raises(RuntimeError) as excinfo:
            generate_meal_kit(wish)
        assert "Failed to generate recipe" in str(excinfo.value)


# additional tests could validate validation logic of Pydantic models if desired

def test_wishlist_validation():
    # missing items should raise
    with pytest.raises(ValueError):
        WishListInput()

    # dietary restrictions accepted
    w = WishListInput(items=["beans"], dietary_restrictions=["Vegan"])
    assert "Vegan" in w.dietary_restrictions
