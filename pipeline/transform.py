import config
import pandas as pd
import json
import re
from pathlib import Path
from urllib.parse import unquote

def transform_mission_index(input_path: Path = config.INDEX_FILE, output_path: Path = config.CLEAN_INDEX_FILE) -> Path:
    """
    Reads the raw mission index JSON, decodes URL-encoded characters,
    normalizes whitespace in mission titles, and saves the cleaned JSON.

    :param input_path: The path to the raw mission index JSON
    :param output_path: The path to save the cleaned JSON
    :return: The path of the saved the cleaned JSON
    """
    # Ensure the clean directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read the raw JSON data from the file
    with open(input_path, "r", encoding="utf-8") as f:
        raw_missions = json.load(f)

    cleaned_missions = {}
    for raw_title, url in raw_missions.items():
        # Decodes the URL encoding on the string key
        decoded = unquote(raw_title)
        # Replaces any underscores or multiple spaces with a single clean space
        cleaned_title = re.sub(r"[_\s]+", " ", decoded).strip()
        # sets the key name
        cleaned_missions[cleaned_title] = url

    # Save the cleaned dictionary to the clean index file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_missions, f, indent=2)

    return output_path

def transform_mission_index_df(mission_index_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the raw mission index DataFrame into a cleaned mission index DataFrame.
    :param mission_index_df: The raw mission index DataFrame
    :return: the cleaned mission index DataFrame
    """
    # Copies the dataframe
    df = mission_index_df.copy()

    # Decodes the URL encoding and clean whitespace and underscores
    df['Mission Title'] = df['Mission Title'].apply(
        lambda x: re.sub(r"[_\s]+", " ", unquote(str(x))).strip()
    )

    return df