import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MINDEE_API_KEY = os.getenv('MINDEE_API_KEY')
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    DEFAULT_BUDGET = float(os.getenv('DEFAULT_BUDGET', 4000))

config = Config() 