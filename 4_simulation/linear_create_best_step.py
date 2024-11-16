import sqlite3
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import json

def main():
    # User-specified distance
    desired_distance = float(input("Enter the desired distance in meters: "))

    # Connect to the database
    db_connection = sqlite3.connect('simulation_data.db')
    cursor = db_connection.cursor()

    # Fetch successful sequences
    cursor.execute('''
        SELECT id, distance FROM walking_sequences WHERE success = 1
    ''')
    sequences = cursor.fetchall()
    if not sequences:
        print("No successful sequences found in the database.")
        return

    sequence_ids = [seq[0] for seq in sequences]
    distances = {seq[0]: seq[1] for seq in sequences}

    # Initialize data structures
    JOINT_ORDER = ["RH", "RK", "RF", "C1", "C2", "CF", "LH", "LK", "LF"]
    steps_data = {}

    # For each step (excluding first and last standing steps)
    for step_order in range(2, 10):  # Steps 2 to 9
        steps_data[step_order] = {joint: [] for joint in JOINT_ORDER}
        steps_data[step_order]['distance'] = []

    # Fetch steps data for each successful sequence
    for sequence_id in sequence_ids:
        cursor.execute('''
            SELECT step_order, RH, RK, RF, C1, C2, CF, LH, LK, LF
            FROM steps_data
            WHERE sequence_id = ? AND step_order BETWEEN 2 AND 9
            ORDER BY step_order
        ''', (sequence_id,))
        steps = cursor.fetchall()
        if len(steps) != 8:
            continue  # Skip sequences that don't have all steps

        for step in steps:
            step_order = step[0]
            joint_values = step[1:]
            for i, joint in enumerate(JOINT_ORDER):
                steps_data[step_order][joint].append(joint_values[i])
            steps_data[step_order]['distance'].append(distances[sequence_id])

    # Prepare models for each joint at each step
    models = {}
    for step_order in range(2, 10):
        models[step_order] = {}
        for joint in JOINT_ORDER:
            X = np.array(steps_data[step_order]['distance']).reshape(-1, 1)
            y = np.array(steps_data[step_order][joint])
            if len(np.unique(y)) < 2:
                # Not enough variation to train a model
                models[step_order][joint] = y[0]
            else:
                model = LinearRegression()
                model.fit(X, y)
                models[step_order][joint] = model

    # Generate the new sequence
    new_sequence = []

    # First step is the standing position
    standing_step = {
        "RH": 0,
        "RK": 0,
        "RF": 0,
        "C1": 0,
        "C2": 0.4,
        "CF": 0,
        "LH": 0,
        "LK": 0,
        "LF": 0
    }
    new_sequence.append(standing_step.copy())

    # Generate steps 2 to 9
    for step_order in range(2, 10):
        step = {}
        for joint in JOINT_ORDER:
            model_or_value = models[step_order][joint]
            if isinstance(model_or_value, LinearRegression):
                predicted_value = model_or_value.predict([[desired_distance]])[0]
            else:
                predicted_value = model_or_value  # Use the constant value
            # Apply joint limits if necessary
            # For now, we'll just round the predicted values
            if joint == 'C2':
                step[joint] = round(predicted_value, 3)
            else:
                step[joint] = round(predicted_value)
        # Ensure symmetry between left and right joints
        if joint.startswith('L'):
            corresponding_right_joint = 'R' + joint[1]
            step[joint] = step[corresponding_right_joint]
        new_sequence.append(step)

    # Last step is the standing position
    new_sequence.append(standing_step.copy())

    # Output the sequence as JSON
    output_filename = f"predicted_sequence_{desired_distance:.2f}m.json"
    with open(output_filename, 'w') as outfile:
        json.dump({'steps': new_sequence}, outfile, indent=4)

    print(f"Generated walking sequence saved to {output_filename}")

    # Close the database connection
    db_connection.close()

if __name__ == "__main__":
    main()
