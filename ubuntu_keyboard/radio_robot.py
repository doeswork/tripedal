import serial
import keyboard

# Set up the serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)  # replace '/dev/ttyUSB0' with your Arduino's port

def send_left(event):
    ser.write(b'l')

def send_right(event):
    ser.write(b'r')

keyboard.on_press_key("left", send_left)
keyboard.on_press_key("right", send_right)

# Block the program and listen for key presses
keyboard.wait()
