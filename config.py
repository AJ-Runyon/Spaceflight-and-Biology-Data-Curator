"""
onfig.py - Configuration settings for the program.
"""
from pathlib import Path

# Sets the location of the raw, transformed, and loaded data
RAW_DIR = Path("data/raw_missions")
CLEAN_DIR = Path("data/clean_missions")

# Sets the files for raw and clean mission index JSONs
INDEX_FILE = RAW_DIR / "all_missions_index.json"
CLEAN_INDEX_FILE = CLEAN_DIR / "clean_missions_index.json"

# Sets the API url for OSDR mission data
MISSIONS_INDEX_URL = "https://osdr.nasa.gov/geode-py/ws/api/missions"
# Sets the delay for API requests
# DELAY: float = 0.3

# For politeness
HEADERS = {
    "User-Agent": "Spaceflight-Biology-Data-Curator 0.0.1 (GitHub: AJ-Runyon)"
}