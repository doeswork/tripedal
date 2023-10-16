import serial
import time

DEVICE = '/dev/rfcomm0'
BAUD_RATE = 9600

# Connect to the device
try:
    s = serial.Serial(DEVICE, BAUD_RATE)
    print(f"Connected to {DEVICE}")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

time.sleep(5)  # Give some time for the connection to stabilize

# Send '10' to Arduino to start the servo loop
s.write('a'.encode('utf-8'))

time.sleep(5)  # Give some time for the connection to stabilize

# Close the serial port
s.close()
print("Closed serial connection")

