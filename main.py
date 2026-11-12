import requests
import psycopg

# Configuration variables
BASE_URL = "https://visualization.osdr.nasa.gov/biodata/api/v2/datasets"
# TODO Update with your actual PostgreSQL credentials and make sure information is not committed to Git
DB_CONFIG = "dbname=osdr_db user=postgres password=your_password host=localhost port=5432"

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

# TODO: review and revise
def save_urls_to_postgres(cleaned_urls):
    # Convert dictionary into a list of tuples: [('OSD-1', 'https://...'), ...]
    records = list(cleaned_urls.items())

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
    print(data)
    return data



if __name__ == "__main__":
    raw_data = get_bio_data_urls()
    cleaned_urls= clean_bio_data(raw_data)
    target_url = input("Enter the target accession number: >")
    save_urls_to_postgres(cleaned_urls)
    get_accession_metadata(cleaned_urls, target_url)