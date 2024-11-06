import sqlite3
import pandas as pd
import os
import json

def create_json_from_db(db_name='walking_sequences.db'):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    
    # Ensure the output directory exists
    output_dir = 'json_walking_sequences'
    os.makedirs(output_dir, exist_ok=True)

    # Load steps table into a DataFrame
    steps_df = pd.read_sql_query("SELECT * FROM steps", conn)
    
    # Load walk_test_results table into a DataFrame
    walk_test_results_df = pd.read_sql_query("SELECT * FROM walk_test_results", conn)

    # Get unique walking_sequence_id
    unique_ids = steps_df['walking_sequence_id'].unique()
    
    # Iterate over each unique walking_sequence_id
    for walking_sequence_id in unique_ids:
        # Filter steps by walking_sequence_id and sort by step_order
        filtered_steps = steps_df[steps_df['walking_sequence_id'] == walking_sequence_id].sort_values(by='step_order')
        
        # Prepare the JSON structure
        steps_list = []
        for _, row in filtered_steps.iterrows():
            step = {
                "RH": row['right_hip'],
                "RK": row['right_knee'],
                "RF": row['right_ankle'],
                "C1": row['center_hip'],
                "C2": row['center_knee'],
                "CF": row['center_foot'],
                "LH": row['left_hip'],
                "LK": row['left_knee'],
                "LF": row['left_ankle']
            }
            steps_list.append(step)
        
        steps_json = {"steps": [steps_list]}
        
        # Get the result from walk_test_results for this sequence
        result_row = walk_test_results_df[walk_test_results_df['walking_sequence_id'] == walking_sequence_id]
        result = result_row['result'].iloc[0] if not result_row.empty else None
        result_text = "success" if result == 1 else "fail" if result == 0 else "unknown"
        
        # Define JSON file name
        json_file_name = f"{walking_sequence_id}_{result_text}.json"
        json_file_path = os.path.join(output_dir, json_file_name)
        
        # Write JSON to file
        with open(json_file_path, 'w') as json_file:
            json.dump(steps_json, json_file, indent=2)
    
    # Close the database connection
    conn.close()

    print(f"JSON files have been created in the '{output_dir}' directory.")

# Execute the function
create_json_from_db()
