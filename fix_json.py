import os
import json

# Define the mapping from the actual servo values to the simulation neutral values
NEUTRAL_MAPPING = {
    "RH": 116.0,
    "RK": 123.0,
    "RF": 122.0,
    "C1": 121.0,
    "C2": 90.0,  # Note: This will be mapped to 0.3 in the simulation
    "CF": 90.0,
    "LH": 116.0,
    "LK": 111.0,
    "LF": 121.0
}

SIMULATION_NEUTRAL = {
    "RH": 0,
    "RK": 0,
    "RF": 0,
    "C1": 0,
    "C2": 0.3,  # Special case
    "CF": 0,
    "LH": 0,
    "LK": 0,
    "LF": 0
}

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def clean_step(step):
    cleaned_step = {}
    for key, value in step.items():
        neutral_value = NEUTRAL_MAPPING[key]
        
        # Determine the scaling factor based on the servo type
        if key in ["LH", "RH"]:
            # Scale for hip servos with a 0-300 range
            scale_factor = 1.67
        elif key in ["LK", "RK"]:
            # Scale for knee servos with a 0-270 range
            scale_factor = 1.5
        else:
            # No scaling for other servos (0-180 range assumed)
            scale_factor = 1.0
        
        # Apply the special handling for C2
        if key == "C2":
            cleaned_step[key] = 0.3 if abs(value - neutral_value) < 1e-2 else round((value / 180) * 0.6, 2)
        elif key == "LF" or key == "RF":
            # For LF and RF, apply adjustment directly and scale
            adjusted_value = (value - neutral_value) * scale_factor
            cleaned_step[key] = SIMULATION_NEUTRAL[key] if abs(value - neutral_value) < 1e-2 else abs(adjusted_value)
        elif key.startswith("L") and key != "LF":
            # For left servos (except LF), invert adjustment (mirror) and scale
            adjusted_value = -(value - neutral_value) * scale_factor
            cleaned_step[key] = SIMULATION_NEUTRAL[key] if abs(value - neutral_value) < 1e-2 else adjusted_value
        else:
            # For right servos, adjust normally and scale
            adjusted_value = (value - neutral_value) * scale_factor
            cleaned_step[key] = SIMULATION_NEUTRAL[key] if abs(value - neutral_value) < 1e-2 else adjusted_value

    return cleaned_step

def clean_walking_sequence(data):
    # Apply the cleaner to each step
    for sequence in data["steps"]:
        for i, step in enumerate(sequence):
            sequence[i] = clean_step(step)
    return data

def main():
    input_dir = 'json_walking_sequences'
    output_dir = 'corrected_json_walking_sequences'
    os.makedirs(output_dir, exist_ok=True)

    # List available JSON files
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    if not json_files:
        print("No JSON files found in the 'json_walking_sequences' directory.")
        return

    # Display available files
    print("Available JSON files:")
    for i, file_name in enumerate(json_files):
        print(f"{i + 1}. {file_name}")

    # Prompt user to select a file
    choice = input("Enter the number of the file you want to clean: ")
    try:
        file_index = int(choice) - 1
        if file_index < 0 or file_index >= len(json_files):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    # Load, clean, and save the selected JSON file
    selected_file = json_files[file_index]
    input_file_path = os.path.join(input_dir, selected_file)
    output_file_path = os.path.join(output_dir, selected_file)

    # Load and clean the JSON data
    data = load_json_file(input_file_path)
    cleaned_data = clean_walking_sequence(data)

    # Save the cleaned JSON data
    save_json_file(cleaned_data, output_file_path)
    print(f"Cleaned JSON saved to '{output_file_path}'.")

if __name__ == '__main__':
    main()
