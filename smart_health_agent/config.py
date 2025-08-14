"""
Configuration settings for Smart Health Agent
"""
import os

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Model configuration
DEFAULT_MODEL = "qwen3:4b"
MODEL_TEMPERATURE = 0.2
ENABLE_STREAMING = True

# RAG configuration
FAISS_DB_PATH = "./faiss_health_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"
SIMILARITY_SEARCH_K = 3
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# UI configuration
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 7860
ENABLE_SHARE = False
ENABLE_DEBUG = False

# Health data thresholds
HEART_RATE_NORMAL_RANGE = (60, 100)
SLEEP_OPTIMAL_RANGE = (7, 9)
ACTIVITY_THRESHOLD = 10000

# Default coordinates (Las Vegas) - used for weather data
DEFAULT_LATITUDE = 36.1699
DEFAULT_LONGITUDE = -115.1398

# Paths
TEMP_UPLOADS_DIR = "temp_uploads"
TABLE_REFERENCES_DIR = "vectorstore/table_references"
IMAGE_REFERENCES_DIR = "vectorstore/image_references"
