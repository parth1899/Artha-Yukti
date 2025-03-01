import os
from dotenv import load_dotenv
import json
from pathlib import Path
import pickle

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama3-70b-8192"
