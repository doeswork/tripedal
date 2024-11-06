import sqlite3
import csv

def export_steps_to_csv(db_name, output_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get all steps
    cursor.execute("SELECT * FROM steps")
    steps = cursor.fetchall()

    # Get column names
    cursor.execute("PRAGMA table_info(steps)")
    columns = [column[1] for column in cursor.fetchall()]

    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(columns)
        
        # Write data
        csvwriter.writerows(steps)

    conn.close()

    print(f"Steps data exported to {output_file}")

if __name__ == '__main__':
    export_steps_to_csv('walking_sequences.db', 'steps.csv')