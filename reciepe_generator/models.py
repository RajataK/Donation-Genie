from typing import List, Optional
from pydantic import BaseModel, Field

class WishListInput(BaseModel):
    items: List[str] = Field(..., description="List of items currently needed by the food bank")
    staples_available: bool = Field(default=True, description="Assume recipient has salt, pepper, oil, water")
    dietary_restrictions: Optional[List[str]] = Field(
        default=None, 
        description="E.g., ['Vegetarian', 'Gluten-Free', 'Halal', 'Nut-Free']"
    )

class Ingredient(BaseModel):
    item: str
    quantity: str
    is_from_wishlist: bool
    notes: Optional[str] = None

class RecipeStep(BaseModel):
    step_number: int
    instruction: str

class MealKit(BaseModel):
    kit_name: str = Field(..., description="A catchy, emotional name for the meal kit")
    impact_message: str = Field(..., description="A 1-2 sentence statement on the emotional value of this donation")
    description: str
    difficulty_level: str = Field(..., description="Easy, Medium, or Hard")
    prep_time_minutes: int
    servings: int
    ingredients: List[Ingredient]
    instructions: List[RecipeStep]
    missing_items_suggestion: Optional[str] = Field(None, description="One low-cost item the donor could add")
