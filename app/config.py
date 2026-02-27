import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

USE_BIGQUERY = True

BIGQUERY_PROJECT = "project-1ea86068-2bc5-4bb0-8af"

DEFAULT_LIMIT = 100
