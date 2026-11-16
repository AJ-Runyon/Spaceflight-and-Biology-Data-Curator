import requests
import psycopg
import json
from pathlib import Path

# Configuration variables
BASE_URL = "https://visualization.osdr.nasa.gov/biodata/api/v2/datasets"
# TODO Update with your actual PostgreSQL credentials and make sure information is not committed to Git
DB_CONFIG = "dbname=osdr_db user=postgres password=your_password host=localhost port=5432"
MISSIONS_LIST_URL = "https://osdr.nasa.gov/geode-py/ws/api/missions"
HEADERS = {
    "User-Agent": "Spaceflight-Biology-Data-Curator 0.0.1 (GitHub: AJ-Runyon)"
}
OUTPUT_FILE = Path("data/raw_missions/all_mission_details.json")

def script_logging():
    """
    :input:
    :return:
    """
    pass

# EXTRACT FUNCTIONS

def extract_mission_data_list():
    """
    :return: dictionary of mission urls
    """
    # Fetches the master list of all missions
    response = requests.get(MISSIONS_LIST_URL, timeout=20)
    response.raise_for_status()
    missions_index = response.json()
    print(f"{missions_index}")

    # Saves the raw mission list locally to Json
    with open("all_missions_index.json", "w", encoding="utf-8") as f:
        json.dump(missions_index, f, indent=2)

    print("Saved master missions index to all_missions_index.json")
    return missions_index

# TRANSFORM FUNCTIONS

def get_mission_api_urls(json_filepath: str | Path = "all_missions_index.json") -> list[str]:
    """
    Takes in the master list of API Urls and outputs a clean list of mission urls.

    :param json_filepath: all_missions_index.json
    :return: clean list of individual mission API URLs
    """


    with open(json_filepath, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # Unwraps the data key if the JSON is a dict, otherwise iterate the list directly
    entries = index_data.get("data", []) if isinstance(index_data, dict) else index_data

    mission_urls = []
    for entry in entries:
        if isinstance(entry, dict):
            # NASA GEODE stores the endpoint string under the "mission" key
            url = entry.get("mission") or entry.get("REST_URL")
            if url:
                mission_urls.append(url)
        elif isinstance(entry, str):
            mission_urls.append(entry)

    return mission_urls

def transform_mission_data(mission_data):
    """
    :input: messy mission data
    :return: cleaned and transformed data
    """
    pass

def save_to_mission_dataset():
    """
    :input: raw data
    :return: json of the raw data
    """
    pass


def load_to_mission_dataset():
    """
    :input: transformed mission data
    :return: loaded dataset into the relational database for mission data
    """
    pass

def sql_quering():
    """
    :input: Takes in SQL commands
    :return: outputs the retrived data from the mission database
    """
    pass



def get_bio_data_urls():
    # Request JSON format instead of the HTML browser view
    all_datasets_url = f"{BASE_URL}/?format=json"
    response = requests.get(all_datasets_url)
    response.raise_for_status()  # Raises an error if the request failed
    print("Successfully retrieved data")
    bio_data_all = response.json()
    return bio_data_all

def clean_bio_data(bio_data_all):
    # Flattens the data so it can be used easer later.
    accession_urls = {
        accession: details["REST_URL"]
        for accession, details in bio_data_all.items()
    }
    print("Successfully cleaned accession urls")
    return accession_urls


def save_urls_to_postgres(cleaned_url):
    # Convert dictionary into a list of tuples: [('OSD-1', 'https://...'), ...]
    records = list(cleaned_url.items())

    # Connect using context managers (automatically commits and closes)
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # 1. Create the table if it doesn't exist yet
            cur.execute("""
                CREATE TABLE IF NOT EXISTS datasets (
                    accession VARCHAR(20) PRIMARY KEY,
                    rest_url TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Bulk insert or update existing records
            cur.executemany("""
                INSERT INTO datasets (accession, rest_url)
                VALUES (%s, %s)
                ON CONFLICT (accession) 
                DO UPDATE SET 
                    rest_url = EXCLUDED.rest_url,
                    updated_at = CURRENT_TIMESTAMP;
            """, records)

    print(f"Successfully saved {len(records)} datasets to PostgreSQL.")

def get_accession_metadata(cleaned_urls, user_input):
    # Normalize input so both "1" and "OSD-1" work
    key = user_input.strip().upper()
    if not key.startswith("OSD-"):
        key = f"OSD-{key}"

    # Look up the exact REST_URL from your cleaned dictionary
    url = cleaned_urls.get(key)
    if not url:
        print(f"Error: {key} was not found in the dataset list.")
        return None

    response = requests.get(url)
    response.raise_for_status()
    print(f"Successfully retrieved metadata for {key}")
    data = response.json()
    # print(data)
    return data



if __name__ == "__main__":
    extract_mission_data_list()
    urls = get_mission_api_urls("all_missions_index.json")
    print(f"Extracted {len(urls)} mission URLs.")
    print("First 5 URLs:", urls[:5])