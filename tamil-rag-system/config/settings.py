"""
Configuration settings for Tamil RAG System
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEXTBOOKS_DIR = DATA_DIR / "textbooks"
PROCESSED_DIR = DATA_DIR / "processed"

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", 1536))
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.1))

# Memgraph Cloud settings
MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "localhost")
MEMGRAPH_PORT = int(os.getenv("MEMGRAPH_PORT", 7687))
MEMGRAPH_USERNAME = os.getenv("MEMGRAPH_USERNAME", "")
MEMGRAPH_PASSWORD = os.getenv("MEMGRAPH_PASSWORD", "")
MEMGRAPH_ENCRYPTED = os.getenv("MEMGRAPH_ENCRYPTED", "true").lower() == "true"

# Vector index configuration
VECTOR_INDEX_CONFIG = {
    "dimension": EMBEDDING_DIMENSIONS,
    "capacity": 50000,
    "metric": "cos",
    "resize_coefficient": 2
}

# Debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


def validate_config():
    """Validate that all required configuration is present."""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set")
    
    if not MEMGRAPH_PASSWORD:
        errors.append("MEMGRAPH_PASSWORD is not set")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True


if __name__ == "__main__":
    validate_config()
    print("✅ Configuration validated successfully!")
    print(f"   Project Root: {PROJECT_ROOT}")
    print(f"   Embedding Model: {EMBEDDING_MODEL}")
    print(f"   LLM Model: {LLM_MODEL}")
    print(f"   Memgraph: {MEMGRAPH_HOST}:{MEMGRAPH_PORT} (SSL: {MEMGRAPH_ENCRYPTED})")