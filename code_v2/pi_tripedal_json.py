from adafruit_servokit import ServoKit
import json
import time
import glob

kit = ServoKit(channels=16)

# Function to adjust knee (calf) angle
def adjust_knee_angle(knee_angle):
    # Convert (-105, 105) to (0, 270)
    return int((knee_angle + 105) * 270 / 210)

# Function to adjust C2 angle
def adjust_c2_angle(c2_angle):
    # Convert (0.0, 0.4) to (0, 270)
    return int(c2_angle * 270 / 0.4)

# Function to adjust other angles
def adjust_other_angle(angle):
    # Convert (-90, 90) to (0, 180)
    return int((angle + 90) * 180 / 180)

def set_servo_positions_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        for step in data['steps']:
            servo_positions = {}
            for joint, angle in step.items():
                if joint in ['RK', 'LK']:  # Knee joints
                    servo_positions[joint] = adjust_knee_angle(angle)
                elif joint == 'C2':  # C2 joint
                    servo_positions[joint] = adjust_c2_angle(angle)
                else:  # Other joints
                    servo_positions[joint] = adjust_other_angle(angle)
            
            # Map the joint names to their respective servo channels
            servo_map = {
                'RH': 0, 'RK': 1, 'RF': 2,
                'C1': 3, 'C2': 4, 'CF': 5,
                'LH': 6, 'LK': 7, 'LF': 8,
            }
            
            # Set servo positions
            for joint, angle in servo_positions.items():
                if joint in servo_map:
                    servo_channel = servo_map[joint]
                    kit.servo[servo_channel].angle = angle
                    print(f"Moving servo {servo_channel} ({joint}) to {angle} degrees.")
                else:
                    print(f"Invalid joint name: {joint}. Skipping...")

            # Add a delay between steps to allow time for the movement to complete
            time.sleep(1.6)  # Adjust the sleep time as needed

if __name__ == "__main__":
    # Search for JSON files in the current directory
    json_files = glob.glob('*.json')

    if not json_files:
        print("No JSON files found in the current directory.")
    else:
        print("Available JSON files:")
        for idx, file in enumerate(json_files):
            print(f"{idx + 1}. {file}")

        # Let the user select a JSON file
        selection = input("Enter the number of the JSON file you want to use: ")
        try:
            selection_idx = int(selection) - 1
            if 0 <= selection_idx < len(json_files):
                json_file_path = json_files[selection_idx]
                set_servo_positions_from_json(json_file_path)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
