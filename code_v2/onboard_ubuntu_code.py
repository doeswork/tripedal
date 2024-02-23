import time
import csv
from adafruit_servokit import ServoKit

# Specify the number of channels on your PCA9685 board
kit = ServoKit(channels=16)

def control_servo(servo_number, angle):
    """
    Controls a single servo.

    :param servo_number: The servo number (0-15) to control.
    :param angle: The angle to set for the servo (0-180 degrees for thigh and foot, 0-270 for calf).
    """
    # For calf servos at positions 1, 4, and 7, adjust the angle if necessary
    if servo_number in [1, 4, 7] and 0 <= angle <= 270:
        # Map 0-270 range to 0-180
        angle = angle * (180/270)
    if 0 <= servo_number <= 15 and 0 <= angle <= 180:
        print(f"Moving servo {servo_number} to {angle:.2f} degrees.")
        kit.servo[servo_number].angle = angle
    else:
        print("Invalid servo number or angle. Please choose a servo number between 0-15 and angle within the valid range.")

def move_servos_from_csv(csv_file_path):
    """
    Reads servo angles from a CSV file and moves the servos to those angles.

    :param csv_file_path: Path to the CSV file containing servo angles.
    """
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:  # Ensure the row is not empty
                # Assuming the CSV file rows are formatted as:
                # 1_Thigh_Angle,1_Calf_Angle,1_Foot_Angle,2_Thigh_Angle,2_Calf_Angle,2_Foot_Angle,3_Thigh_Angle,3_Calf_Angle,3_Foot_Angle
                for i, angle_str in enumerate(row):
                    angle = float(angle_str)  # Convert angle to float
                    control_servo(i, angle)
                time.sleep(1)  # Wait a second before moving to the next row of angles

# Example usage
if __name__ == "__main__":
    csv_file_path = 'path_to_your_csv_file.csv'  # Update this to your CSV file path
    move_servos_from_csv(csv_file_path)
