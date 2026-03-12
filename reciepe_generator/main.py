from fastapi import FastAPI, HTTPException
from models import WishListInput, MealKit
from generator import generate_meal_kit

app = FastAPI(
    title="Food Bank Meal Kit Generator",
    version="1.1.0-feature-dietary",
    description="AI-powered engine to convert donations into actionable meal kits."
)

@app.post("/generate-kit", response_model=MealKit)
async def create_meal_kit(payload: WishListInput):
    """
    Takes a list of food bank needs and optional dietary preferences 
    and converts them into a persuasive Meal Kit donation opportunity.
    """
    if not payload.items:
        raise HTTPException(status_code=400, detail="Wish list cannot be empty.")
    
    try:
        # Generate the kit
        meal_kit = generate_meal_kit(payload)
        return meal_kit
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

if __name__ == "__main__":
    import uvicorn
    # Reload is enabled for easier development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
