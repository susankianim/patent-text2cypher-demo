import os
from dotenv import load_dotenv

# Load variables from .env file.
load_dotenv()

# Toggle to True to print full stack traces in case of unexpected errors
DEBUG = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gemini-2.5-flash")
OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", 
    "https://generativelanguage.googleapis.com/v1beta/openai/"
)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def check_environment_variables() -> None:
    """
    Check required environment variables before running the demo.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing in .env file.")

    if not NEO4J_PASSWORD:
        raise RuntimeError("NEO4J_PASSWORD is missing in .env file.")
