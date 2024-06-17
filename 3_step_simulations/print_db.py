import sqlite3

def fetch_all_records(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Define the SQL query to select all records
    # query = "SELECT * FROM results"
    query = "SELECT * FROM results WHERE fall != 1"

    try:
        # Execute the query
        cursor.execute(query)

        # Fetch all records
        records = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Print column names
        print(column_names)

        # Print records
        for record in records:
            print(record)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

# Specify the path to the SQLite database
db_path = '4_step_final_simulation_results.db'

# Fetch and print all records from the database
fetch_all_records(db_path)
