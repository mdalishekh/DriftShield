import os
from dotenv import load_dotenv

load_dotenv()

class ENV:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    