# Recipe Generator

A smart meal kit generator powered by OpenAI that converts food bank donation items into cohesive, delicious recipes with emotional impact messaging highlighting dignity and care.

## Overview

The Recipe Generator transforms a list of available food items into complete, executable meal kits. It intelligently:
- Uses only provided wishlist items and available staples
- Respects dietary restrictions
- Creates recipes appropriate for food bank recipients
- Generates impact messages focused on dignity and care
- Provides detailed cooking instructions with ingredient quantities
- Suggests low-cost enhancement options

## Features

✅ **Wishlist-Based Recipes** - Uses only items you specify, no substitutions needed
✅ **Dietary Compliance** - Strictly adheres to dietary restrictions (Vegan, Gluten-Free, Dairy-Free, etc.)
✅ **Impact Messaging** - Emotional, dignity-focused narratives for each recipe
✅ **Flexible Staples** - Adapts recipes based on whether basic staples are available
✅ **Complete Meal Plans** - Full ingredient lists with quantities and source tracking
✅ **Step-by-Step Instructions** - Easy-to-follow cooking directions
✅ **Accessibility** - Recipes prioritize ease of preparation

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variable:
```bash
export OPENAI_API_KEY=your-api-key-here
```

## Usage

### Command Line

```bash
python generator.py --items "ITEM1, ITEM2, ITEM3" [--diet "RESTRICTION1, RESTRICTION2"] [--staples]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--items` | string | Yes | Comma-separated list of available food items |
| `--diet` | string | No | Comma-separated dietary restrictions (e.g., "Vegan, Gluten-Free") |
| `--staples` | flag | No | Include this flag if basic staples are available (salt, pepper, oil, water) |

### Examples

**Basic Recipe:**
```bash
python generator.py --items "canned beans, rice, onion" --staples
```

**With Dietary Restrictions:**
```bash
python generator.py --items "chickpeas, spinach, sweet potato" --diet "Vegan" --staples
```

**Multiple Restrictions:**
```bash
python generator.py --items "peanut butter, banana, oats" --diet "Gluten-Free, Dairy-Free" --staples
```

**Limited Resources (water only):**
```bash
python generator.py --items "lentils, carrots, cabbage"
```

## Output Format

The generator returns a comprehensive JSON structure:

```json
{
  "kit_name": "Recipe Name",
  "impact_message": "Emotional message about dignity and care",
  "description": "Brief overview of the meal",
  "difficulty_level": "Easy|Medium|Hard",
  "prep_time_minutes": 30,
  "servings": 4,
  "ingredients": [
    {
      "item": "ingredient name",
      "quantity": "amount",
      "is_from_wishlist": true/false,
      "notes": "optional preparation notes"
    }
  ],
  "instructions": [
    {
      "step_number": 1,
      "instruction": "Cooking step"
    }
  ],
  "missing_items_suggestion": "Optional enhancement suggestion or null"
}
```

## Configuration

Configuration is managed through `config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4o-mini"  # Can be adjusted for different models
```

## Data Models

### WishListInput
Represents the user's input:
- `items`: List of food items available
- `dietary_restrictions`: Optional list of dietary restrictions
- `staples_available`: Boolean flag for basic cooking staples

### MealKit
Represents the generated recipe output with all fields mentioned in the output format section.

## Key Fixes & Improvements

### JSON Sanitization
OpenAI API responses sometimes include trailing commas in JSON. The generator includes a `sanitize_json()` function that:
- Removes trailing commas before `}` and `]`
- Prevents `JSONDecodeError` exceptions
- Uses regex pattern: `r',(\s*[}\]])'` → `r'\1'`

### Pydantic v2 Compatibility
Updated to use `model_dump_json()` instead of the deprecated `json()` method, ensuring compatibility with Pydantic 2.x+

## Testing

Run tests with:
```bash
pytest
```

Test coverage includes:
- JSON output validation
- Dietary restriction adherence
- Staple availability handling
- Ingredient quantity reasonableness
- Instruction step sequencing

## Architecture

```
generator.py          # Main generation logic with OpenAI integration
├── generate_meal_kit()      # Core function for recipe generation
├── sanitize_json()          # JSON error handling
└── Command-line interface

config.py            # Settings management
models.py            # Pydantic data models (WishListInput, MealKit)
requirements.txt     # Package dependencies
```

## Error Handling

The generator provides clear error messages for common issues:
- Invalid API key → "Failed to generate recipe"
- Malformed JSON from API → Automatically sanitized and retried
- Missing required items → Clear parameter validation

## Performance

- **Average Response Time**: 2-5 seconds (depends on API latency)
- **Model**: GPT-4o-mini (faster, efficient, cost-effective)
- **Temperature**: 0.7 (balanced creativity and consistency)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `MODEL_NAME` | No | `gpt-4o-mini` | OpenAI model to use |

## Contributing

When adding features:
1. Update data models in `models.py` if needed
2. Add corresponding tests in `tests/`
3. Update this README with new parameters/examples
4. Run tests to ensure no regressions

## License

Part of the Donation-Genie project.

## Support

For issues or improvements, please refer to the main Donation-Genie repository documentation.
