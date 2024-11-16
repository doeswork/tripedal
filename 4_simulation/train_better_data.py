import sqlite3
import numpy as np
import tensorflow as tf
import json
import os

    # Convert the sequence to serializable Python types
def convert_to_serializable(obj):
    """Recursively convert NumPy types to native Python types."""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(v) for v in obj]
    elif isinstance(obj, np.integer):  # Handle NumPy int types
            return int(obj)
    elif isinstance(obj, np.floating):  # Handle NumPy float types
        return float(obj)
    else:
        return obj  # Leave other types as-is

def main():
    # Check if a GPU is available
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("GPU is available. Using GPU for training.")
    else:
        print("GPU is not available. Training will use the CPU.")

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
    NUM_STEPS = 8  # Steps 2 to 9

    X = []
    y = []

    # Fetch steps data for each successful sequence
    for sequence_id in sequence_ids:
        cursor.execute('''
            SELECT step_order, RH, RK, RF, C1, C2, CF, LH, LK, LF
            FROM steps_data
            WHERE sequence_id = ? AND step_order BETWEEN 2 AND 9
            ORDER BY step_order
        ''', (sequence_id,))
        steps = cursor.fetchall()
        if len(steps) != NUM_STEPS:
            continue  # Skip sequences that don't have all steps

        # Collect joint angles for the sequence
        joint_angles = []
        for step in steps:
            # step_order = step[0]
            joint_values = step[1:]  # Joint values for this step
            # Ensure symmetry: set left joints equal to right joints
            joint_values = list(joint_values)
            joint_dict = dict(zip(JOINT_ORDER, joint_values))
            for joint in ['LH', 'LK', 'LF']:
                corresponding_right_joint = 'R' + joint[1]
                joint_dict[joint] = joint_dict[corresponding_right_joint]
            joint_values = [joint_dict[joint] for joint in JOINT_ORDER]
            joint_angles.extend(joint_values)
        X.append([distances[sequence_id]])
        y.append(joint_angles)

    if not X or not y:
        print("Insufficient data to train the model.")
        return

    X = np.array(X)
    y = np.array(y)

    # Build the neural network model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(1,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(NUM_STEPS * len(JOINT_ORDER))
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    print("Training the model...")
    history = model.fit(X, y, epochs=500, validation_split=0.2, verbose=0)

    # Optionally, you can visualize the training progress
    # import matplotlib.pyplot as plt
    # plt.plot(history.history['loss'], label='Training Loss')
    # plt.plot(history.history['val_loss'], label='Validation Loss')
    # plt.legend()
    # plt.show()

    # Predict joint angles for the desired distance
    predicted_joint_angles = model.predict([[desired_distance]])[0]

    # Reshape predicted_joint_angles to (NUM_STEPS, len(JOINT_ORDER))
    predicted_joint_angles = predicted_joint_angles.reshape(NUM_STEPS, len(JOINT_ORDER))

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
    for step_idx in range(NUM_STEPS):
        step_values = predicted_joint_angles[step_idx]
        step = {}
        for i, joint in enumerate(JOINT_ORDER):
            value = step_values[i]
            # Apply joint limits and rounding
            if joint == 'C2':
                step[joint] = round(float(value), 3)
                step[joint] = np.clip(step[joint], 0.0, 0.4)
            else:
                step[joint] = round(float(value))
                # Apply joint limits
                if joint in ['RH', 'LH']:
                    step[joint] = np.clip(step[joint], -150, 150)
                elif joint in ['RK', 'LK']:
                    step[joint] = np.clip(step[joint], -135, 135)
                elif joint in ['RF', 'LF']:
                    step[joint] = np.clip(step[joint], -90, 90)
                elif joint in ['C1', 'CF']:
                    step[joint] = np.clip(step[joint], -90, 90)
        # Ensure symmetry between left and right joints
        for joint in ['LH', 'LK', 'LF']:
            corresponding_right_joint = 'R' + joint[1]
            step[joint] = step[corresponding_right_joint]
        new_sequence.append(step)

    # Last step is the standing position
    new_sequence.append(standing_step.copy())

    # Output the sequence as JSON
    output_filename = f"predicted_sequence_{desired_distance:.2f}m.json"
    with open(output_filename, 'w') as outfile:
        serializable_sequence = convert_to_serializable({'steps': new_sequence})
        json.dump(serializable_sequence, outfile, indent=4)

    print(f"Generated walking sequence saved to {output_filename}")

    # Close the database connection
    db_connection.close()

if __name__ == "__main__":
    main()
