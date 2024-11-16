import sqlite3
import numpy as np
import tensorflow as tf
import os

def main():
    # Check if a GPU is available
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("GPU is available. Using GPU for training.")
    else:
        print("GPU is not available. Training will use the CPU.")

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
    print("Model training completed.")

    # Save the trained model
    MODEL_DIR = "trained_model"
    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save(MODEL_DIR)
    print(f"Model saved to {MODEL_DIR}")

    # Close the database connection
    db_connection.close()

if __name__ == "__main__":
    main()
