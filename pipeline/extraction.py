"""
extraction.py - Contains the extraction functions for the program.
"""
import requests
import config
import json
from pathlib import Path
import pandas as pd


def extract_master_list(index_url: str = config.MISSIONS_INDEX_URL, output_path: Path = config.INDEX_FILE) -> Path:
    """
    Extracts a json of all the missions from OSDR with the API urls and their mission titles as messy data.

    :param index_url: The API URL for mission urls
    :param output_path: The path to save the json
    :return: The path of the saved the json
    """
    # Ensures the folder exists for the output.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Sends a GET request to the sever
    response = requests.get(index_url, headers=config.HEADERS, timeout=20)
    # For when the server returns a failure status code
    response.raise_for_status()
    # Stores the data as a json
    index_data = response.json()
    # print(index_data)
    # Attach the keys to the URL where the keys are the mission titles (uncleaned)
    missions_map = {}
    for entry in index_data.get("data", []):
        mission_url = entry.get("mission")
        if mission_url:
            # Extracts the mission title from the end of the URL (e.g., "STS-135" or "SpaceX-12")
            mission_title = mission_url.rstrip("/").split("/")[-1]
            missions_map[mission_title] = mission_url

    # Creates the output file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(missions_map, f, indent=2)

    index_df = pd.DataFrame.from_dict(missions_map, orient='index')
    #print(index_df)
    return output_path,index_df

if __name__ == "__main__":
    extract_master_list()