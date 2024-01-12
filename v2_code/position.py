#  ls /dev | grep rfcomm~
#  sudo rfcomm bind 0 00:22:05:00:56:7E or 98:DA:60:07:D9:C7

import serial
import time

DEVICE = '/dev/rfcomm1'
BAUD_RATE = 9600

# Define the positions for the 9 servos
servo_positions = [180, 90, 90, 95, 85, 105, 95, 90, 90]  # Example positions

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
