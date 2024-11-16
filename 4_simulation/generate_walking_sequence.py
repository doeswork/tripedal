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
    # Load the saved model
    MODEL_DIR = "trained_model"
    if not os.path.exists(MODEL_DIR):
        print(f"Model directory '{MODEL_DIR}' does not exist. Please train the model first.")
        return

    model = tf.keras.models.load_model(MODEL_DIR)
    print(f"Model loaded from {MODEL_DIR}")

    # User-specified distance
    desired_distance = float(input("Enter the desired distance in meters: "))

    # Constants
    JOINT_ORDER = ["RH", "RK", "RF", "C1", "C2", "CF", "LH", "LK", "LF"]
    NUM_STEPS = 8  # Steps 2 to 9

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

if __name__ == "__main__":
    main()
