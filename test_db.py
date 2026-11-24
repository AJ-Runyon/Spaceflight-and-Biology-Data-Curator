# ==========================================
# ABOUT: This script is to verify that you can reach PostgreSQL, execute a query, and write as well as read a test table
# ==========================================
import os
import psycopg
from dotenv import load_dotenv

# loads the credentials from  the .env file
load_dotenv()

conn_info = (
    f"host={os.getenv('DB_HOST')} "
    f"port={os.getenv('DB_PORT')} "
    f"dbname={os.getenv('DB_NAME')} "
    f"user={os.getenv('DB_USER')} "
    f"password={os.getenv('DB_PASSWORD')}"
)

def verify_connection():
    try:
        # Automatically closes the connection
        with psycopg.connect(conn_info) as conn:
            # Automatically commits transactions if no errors occur
            with conn.cursor() as cur:
                # Checks the server version
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"Connected successfully!\nServer: {version}\n")

                #  Creates a temporary table
                cur.execute("""
                    CREATE TEMP TABLE connection_test (
                        id SERIAL PRIMARY KEY,
                        status TEXT
                    );
                """)
                # Tests an SQL command on the temporary table to verify
                cur.execute(
                    "INSERT INTO connection_test (status) VALUES (%s) RETURNING id;",
                    ("OSDR pipeline ready",)
                )
                # Stores the row zero data to be used in the print command
                row_id = cur.fetchone()[0]
                # Makes sure the things function as indented
                print(f"Write test passed (inserted row ID: {row_id}).")

    # In case something goes wrong
    except psycopg.OperationalError as e:
        print(f"Connection failed. Check that the PostgreSQL Windows service is running and .env credentials match.\nError: {e}")

if __name__ == "__main__":
    verify_connection()