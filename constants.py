import os
from dotenv import load_dotenv
from google import genai as genai_google
import google.generativeai as genai
from google.genai.types import Tool, GoogleSearch
import json

# Load environment variables from .env file
load_dotenv(".env")

# Configure API KEY
GEN_AI_API_KEY = os.getenv('GEN_AI_API_KEY')
UNCOMTRADE_SUBS_KEY = os.getenv("UNCOMTRADE_SUBS_KEY")

# Configure the Generative AI model
# MODEL_NAME = "gemini-2.5-flash-preview-05-20"
MODEL_NAME = "gemini-2.0-flash-lite"
client = genai_google.Client(api_key=GEN_AI_API_KEY)
MODEL_GENERATIVE = genai.GenerativeModel(model_name=MODEL_NAME)
GOOGLE_SEARCH_TOOL = Tool(google_search = GoogleSearch())

# Configure OCR variable
with open('data/hs_code_labels.json', 'r') as f:
    HS_CODE_LABELS = json.load(f)

# Configure export trend variable
with open('data/country_to_continent.json', 'r') as f:
    COUNTRY_TO_CONTINENT = json.load(f)