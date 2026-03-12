import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # switching from Google GenAI to OpenAI Chat API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # you can change this to gpt-4 or another available ChatGPT model
    MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

settings = Settings()

if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
