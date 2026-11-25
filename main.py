import sys
from db import verify_connection
from utilities import clear_screen
from pipeline import *

#TODO add logging function

def initialize_pipeline():
    """Starts up the ETL pipeline."""
    clear_screen()
    print("Starting ETL pipeline..")
    # Grabs only the dataframe
    _, mission_df = extract_master_list()
    # Grabs only the dictionary
    mission_api_urls, _ = extract_master_list()
    #print(f"{mission_df}")
    # TODO finish this function
    mission_df = transform_mission_index_df(mission_df)
    clean_file_path = transform_mission_index(mission_api_urls)
    print(f"{clean_file_path}")
    # TODO create and wire in the load module.


def main():
    """Starts up the program loop."""
    running = True

    try:
        while running:
            print(
                "What would you like to do?:\n\n  1. Initialize the ETL Pipeline\n  2. Query the Database\n  3. exit\n\n")
            user_input = input("Enter your choice: >").strip().lower()
            if user_input == "1":
                clear_screen()
                #  Checks the connection before running network or disk operations
                if not verify_connection():
                    print("Aborting program: database is unreachable.")
                    sys.exit(1)
                # Starts up the pipeline
                initialize_pipeline()
            elif user_input == "2":
                clear_screen()
                print("Database querying not implemented yet.")
            elif user_input == "3":
                clear_screen()
                print("Exiting...")
                running = False
                sys.exit(0)
            else:
                clear_screen()
                print("Invalid input. Please enter '1' or '2' or '3'.")

    except (KeyboardInterrupt, EOFError):
        clear_screen()
        print("Exiting...")



if __name__ == "__main__":
    main()