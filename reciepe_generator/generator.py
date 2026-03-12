import json
from openai import OpenAI
import sys
import re
from pathlib import Path

# Add the current directory to sys.path so we can import sibling modules
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from models import WishListInput, MealKit

# Configure OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def sanitize_json(json_string: str) -> str:
    """Remove trailing commas from JSON strings to fix OpenAI response formatting issues."""
    # Remove trailing commas before } and ]
    sanitized = re.sub(r',(\s*[}\]])', r'\1', json_string)
    return sanitized

def generate_meal_kit(wish_list: WishListInput) -> MealKit:
    # Construct the dietary string
    dietary_context = ""
    if wish_list.dietary_restrictions:
        dietary_context = f"CRITICAL DIETARY RESTRICTIONS: {', '.join(wish_list.dietary_restrictions)}. The recipe MUST adhere to these."

    staples_context = "Water, Salt, Pepper, Vegetable Oil" if wish_list.staples_available else "Water only"

    system_prompt = f"""
    You are a creative chef and a non-profit copywriter.
    
    GOAL: Convert a list of food bank wish list items into a cohesive, delicious "Meal Kit" recipe.
    
    INPUT ITEMS: {", ".join(wish_list.items)}
    AVAILABLE STAPLES: {staples_context}
    {dietary_context}
    
    CONSTRAINTS:
    1. STRICTLY use the provided 'INPUT ITEMS' and 'AVAILABLE STAPLES'. 
    2. Do NOT include fresh produce, dairy, or meat unless explicitly listed in INPUT ITEMS.
    3. If dietary restrictions are provided, strictly follow them.
    4. "Impact Message" must be emotional and focused on dignity and care.
    
    OUTPUT FORMAT: Return ONLY valid JSON (no markdown, no explanation) matching this exact schema:
    {{
        "kit_name": "Catchy meal name",
        "impact_message": "1-2 sentence emotional impact statement focused on dignity and care",
        "description": "Brief description of the meal",
        "difficulty_level": "Easy|Medium|Hard",
        "prep_time_minutes": 30,
        "servings": 4,
        "ingredients": [
            {{"item": "ingredient name", "quantity": "amount", "is_from_wishlist": true, "notes": "optional notes"}},
            {{"item": "ingredient name", "quantity": "amount", "is_from_wishlist": false, "notes": null}}
        ],
        "instructions": [
            {{"step_number": 1, "instruction": "First step"}},
            {{"step_number": 2, "instruction": "Second step"}}
        ],
        "missing_items_suggestion": "Optional low-cost item suggestion or null"
    }}
    """

    try:
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.7,
        )

        text = response.choices[0].message.content
        # Sanitize JSON to remove trailing commas
        text = sanitize_json(text)
        response_data = json.loads(text)
        # Handle case where model wraps response in "MealKit" key
        if "MealKit" in response_data:
            response_data = response_data["MealKit"]
        return MealKit(**response_data)

    except Exception as e:
        # In production, you might log this error to a monitoring service
        print(f"OpenAI Error: {e}")
        raise RuntimeError("Failed to generate recipe. Please check inputs or try again.")


# quick command‑line/interactive driver so you can exercise the function with
# real data without writing an extra script.  Usage:
#
#   OPENAI_API_KEY=sk-… python -m reciepe_generator.generator
#
# it will prompt you for comma‑separated wish list items and optional
# dietary restrictions.
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a meal kit from a wish list")
    parser.add_argument("--items", help="Comma-separated wish list items", required=True)
    parser.add_argument("--diet", help="Comma-separated dietary restrictions", default="")
    parser.add_argument("--staples", action="store_true", help="Indicate staples available")

    args = parser.parse_args()

    wish = WishListInput(
        items=[i.strip() for i in args.items.split(",") if i.strip()],
        staples_available=args.staples,
        dietary_restrictions=[d.strip() for d in args.diet.split(",") if d.strip()] or None,
    )

    kit = generate_meal_kit(wish)
    print(kit.model_dump_json(indent=2))
