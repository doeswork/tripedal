import sqlite3
import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# Enable logging to confirm GPU usage
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # Enable all logs
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'  # Allow dynamic memory allocation
tf.debugging.set_log_device_placement(True)

def load_data_for_generation(db_path="simulation_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load successful simulations only
    cursor.execute("SELECT distance, data FROM simulations WHERE success = 1")
    rows = cursor.fetchall()
    conn.close()

    print(f"Loaded {len(rows)} rows from the database.")  # Debug: Check row count

    X = []  # Distances
    y = []  # Joint positions
    for distance, data in rows:
        try:
            # Parse JSON data
            data_json = json.loads(data)
            # If data_json is a dict with 'steps', extract steps; otherwise, assume it's already a list of steps
            if isinstance(data_json, dict) and 'steps' in data_json:
                steps = data_json['steps']
            elif isinstance(data_json, list):
                steps = data_json
            else:
                raise ValueError("Unexpected data format")

            # Flatten joint positions into a single feature vector
            feature_vector = []
            for step in steps:
                if isinstance(step, dict):
                    feature_vector.extend(step.values())  # Combine all joint values
                else:
                    raise ValueError("Step is not a dictionary")

            X.append([float(distance)])  # Distance as the input feature
            y.append(feature_vector)     # Joint positions as the target
        except (TypeError, json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Skipping record due to error: {e}")
            print(f"Problematic data: {data}")
            continue

    print(f"Prepared {len(X)} valid samples.")  # Debug: Check valid samples count
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

# Build the generative model
def build_generative_model(input_shape, output_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(output_shape, activation='linear')
    ])
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    return model

def main():
    # Print GPU availability
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("GPUs Available: ", gpus)
    else:
        print("No GPUs found. Please ensure that the correct version of CUDA and cuDNN are installed.")

    # Load and preprocess data
    X, y = load_data_for_generation()

    # Check for empty datasets
    if len(X) == 0 or len(y) == 0:
        print("No valid data available for training. Exiting.")
        return

    # Split into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize input (distance)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    # Build and train the model
    model = build_generative_model(input_shape=X_train.shape[1], output_shape=y_train.shape[1])

    # Add a print statement to confirm that the model is built
    print("Model summary:")
    model.summary()

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,          # Increased epochs
        batch_size=16,       # Decreased batch size
        verbose=1
    )

    # Save the model and scaler
    model.save("walking_sequence_generator.keras")
    print("Model saved to 'walking_sequence_generator.keras'.")

    scaler_params = {
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
    }
    with open("scaler.json", "w") as f:
        json.dump(scaler_params, f)
    print("Scaler parameters saved to 'scaler.json'.")

    # Debugging output
    print(f"Training completed. Final validation loss: {history.history['val_loss'][-1]:.4f}")

if __name__ == "__main__":
    main()
