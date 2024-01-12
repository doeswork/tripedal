import serial
import time

DEVICE = '/dev/rfcomm0'
BAUD_RATE = 9600

# Define the positions for the 9 servos
servo_positions = [90, 90, 90, 90, 90, 90, 90, 90, 90]  # Example positions

try:
    with serial.Serial(DEVICE, BAUD_RATE, timeout=1) as s:
        print(f"Connected to {DEVICE}")

        time.sleep(5)  # Give some time for the connection to stabilize

        # Convert the list of positions to a comma-separated string
        positions_str = ','.join(map(str, servo_positions))

        # Send the positions to the Arduino
        s.write(positions_str.encode('utf-8'))

        time.sleep(5)  # Give some time for the positions to be applied

        print("Sent servo positions")
except Exception as e:
    print(f"Failed to connect or send data: {e}")

print("Closed serial connection")
