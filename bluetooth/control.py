import serial
# The walking sequence you want to send
#sudo chmod 666 /dev/rfcomm0
#ls /dev | grep rfcomm
#sudo rfcomm bind 0 00:22:05:00:56:7E
# ls /dev | grep rfcomm

# The walking sequence you want to send
STEPS_COUNT = 7
print(f"STEPS_COUNT set to {STEPS_COUNT}")  # Debug print

steps = [
    [0, -15, 15, -10, 10, 0, 0],
    [0, 0, 0, 0, 0, 0, -180],
    [-40, 0, 0, 0, 0, 0, 0],
    [0, -25, 25, -10, 10, 20, 0],
    [40, 0, 0, 0, 0, -20, 0],
    [0, 0, 0, 0, 0, 0, 180],
    [0, 40, -40, 20, -20, 0, 0]
]

DEVICE = '/dev/rfcomm0'
BAUD_RATE = 9600

def send_walking_sequence(s, steps_count, steps):
    data_str = f"{steps_count}"
    for step in steps:
        step_str = ",".join(map(str, step))
        data_str += f",{step_str}"
    data_str += "\n"
    print(f"Sending data: {data_str}")  # Debug print
    s.write(data_str.encode('utf-8'))  # Convert the string to bytes

# Connect to the device
try:
    s = serial.Serial(DEVICE, BAUD_RATE)
    print(f"Connected to {DEVICE}")  # Debug print
    send_walking_sequence(s, STEPS_COUNT, steps)
except Exception as e:
    print(f"Failed to connect: {e}")  # Debug print
    exit(1)

print("Preparing to send walking sequence")  # Debug print

# Send walking sequence to Arduino
send_walking_sequence(s, STEPS_COUNT, steps)

print("Sent walking sequence")  # Debug print

# Close the serial port
s.close()
print("Closed serial connection")  # Debug print
