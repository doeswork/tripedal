from adafruit_servokit import ServoKit
import csv
import time
import glob

kit = ServoKit(channels=16)

def adjust_calf_angle(calf_angle):
    # Map 270 degrees range to 180 degrees
    return int((calf_angle / 270.0) * 180.0)

def set_servo_positions_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            servo_positions = [int(angle) for angle in row]

            # Adjust angles for calf servos
            servo_positions[1] = adjust_calf_angle(servo_positions[1])  # First calf
            servo_positions[4] = adjust_calf_angle(servo_positions[4])  # Second calf
            servo_positions[7] = adjust_calf_angle(servo_positions[7])  # Third calf

            # Set servo positions
            for i, angle in enumerate(servo_positions):
                if 0 <= i <= 8:  # Ensure we're addressing the correct servos
                    kit.servo[i].angle = angle
                    print(f"Moving servo {i} to {angle} degrees.")
                else:
                    print(f"Invalid servo index: {i}. Skipping...")

            # Add a delay between rows to allow time for the movement to complete
            time.sleep(1.6)  # Adjust the sleep time as needed

if __name__ == "__main__":
    # Search for CSV files in the current directory
    csv_files = glob.glob('*.csv')

    if not csv_files:
        print("No CSV files found in the current directory.")
    else:
        print("Available CSV files:")
        for idx, file in enumerate(csv_files):
            print(f"{idx + 1}. {file}")

        # Let the user select a CSV file
        selection = input("Enter the number of the CSV file you want to use: ")
        try:
            selection_idx = int(selection) - 1
            if 0 <= selection_idx < len(csv_files):
                csv_file_path = csv_files[selection_idx]
                set_servo_positions_from_csv(csv_file_path)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")