import sqlite3
import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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
            steps = json.loads(data)  # Treat `data` as a list of step dictionaries
            # Flatten joint positions into a single feature vector
            feature_vector = []
            for step in steps:
                feature_vector.extend(step.values())  # Combine all joint values
            X.append([distance])  # Distance as the input feature
            y.append(feature_vector)  # Joint positions as the target
        except (TypeError, json.JSONDecodeError, KeyError) as e:
            print(f"Skipping record due to error: {e}")
            print(f"Problematic data: {data}")
            continue

    print(f"Prepared {len(X)} valid samples.")  # Debug: Check valid samples count
    return np.array(X), np.array(y)


# Build the generative model
def build_generative_model(input_shape, output_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(output_shape, activation='linear')  # Predict joint positions
    ])
    model.compile(
        optimizer='adam',
        loss='mse',  # Mean squared error for regression
        metrics=['mae']  # Mean absolute error for evaluation
    )
    return model

def main():
    # Load and preprocess data
    X, y = load_data_for_generation()
    
    # Split into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize input (distance)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    # Build and train the model
    model = build_generative_model(input_shape=X_train.shape[1], output_shape=y_train.shape[1])
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=32
    )

    # Save the model and scaler
    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=['mae'])
    model.save("walking_sequence_generator.keras")
    np.save("scaler_mean.npy", scaler.mean_)
    np.save("scaler_scale.npy", scaler.scale_)
    print("Model and scaler saved.")

    scaler_params = {
    "mean": scaler.mean_.tolist(),
    "scale": scaler.scale_.tolist(),
      }
    
    with open("scaler.json", "w") as f:
        json.dump(scaler_params, f)
    print("Scaler parameters saved to 'scaler.json'")

if __name__ == "__main__":
    main()
