import serial
import time
# ls /dev/ttyUSB*
def send_steps_to_arduino(steps, serial_port='/dev/ttyUSB0', baud_rate=9600):
    # Initialize the serial connection
    ser = serial.Serial(serial_port, baud_rate)
    time.sleep(2)  # Wait for the Arduino to initialize

    # Signal start
    ser.write(b'start\n')
    time.sleep(0.5)

    # Send the steps
    for step in steps:
        step_str = ','.join(map(str, step)) + '\n'
        ser.write(step_str.encode())
        time.sleep(0.5)  # Give time for the Arduino to process the data

    # Signal end
    ser.write(b'run\n')

# Define your steps
# steps = [
#     [0, -50, 50, 0, 0, 0, 0],
#     [-180, 0, 0, -20, 20, 0, 0],
#     [0, 0, 0, 0, 0, -70, 0],
#     [0, 50, -50, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 30, 0],
#     [0, 0, 0, 20, -20, 40, 0],
#     [180, 0, 0, 0, 0, 0, 0]
# ]
# steps = [
#     [0, -50, 50, 0, 0, 0, 0],
#     [-20, 0, 0, -20, 20, 0, 0],
#     [0, 0, 0, 0, 0, -20, 0],
#     [0, 50, -50, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 10, 0],
#     [0, 0, 0, 20, -20, 10, 0],
#     [20, 0, 0, 0, 0, 0, 0]
# ]

# waist, thigh, thigh,out knee ,out knee , ankle, liniar knee
# steps = [
#      [0, 50, -50, 0, 0, 0, 0],
#     [-20, 0, 0, -20, 20, 0, 0],
#     [0, 0, 0, 0, 0, -20, 0],
#     [0, -50, 50, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 10, 0],
#     [0, 0, 0, 20, -20, 10, 0],
#     [20, 0, 0, 0, 0, 0, 0]
# ]

#     [0, 0, 0, 0, 0, 0, 0],
steps = [
    # [0, -15, 15, -10, 10, 0, 0],
    # [0, 0, 0, 0, 0, 0, -180],
    # [-40, 0, 0, 0, 0, 0, 0],
    # [0, -25, 25, -10, 10, 20, 0],
    # [40, 0, 0, 0, 0, -20, 0],
    # [0, 0, 0, 0, 0, 0, 180],
    # [0, 40, -40, 20, -20, 0, 0]
]
# Update the serial_port and baud_rate as per your Arduino setup
send_steps_to_arduino(steps, serial_port='/dev/ttyUSB0', baud_rate=9600)
