import keyboard
import serial
import time

# Set up the serial connection
print("Setting up serial connection...")
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change this to the appropriate port for your Arduino Nano
time.sleep(2)  # Wait for the connection to be established

# Check if the serial connection is open
if ser.isOpen():
    print("Serial connection established!")
else:
    print("Failed to establish serial connection.")
    sys.exit()

while True:
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('7'):
        ser.write(b'7')
        time.sleep(0.1) 
        print("Sent '7' command to turn the servo left")
    if keyboard.is_pressed('8'):
        ser.write(b'8')
        time.sleep(0.1) 
        print("Sent '8' command to turn the servo right")
    if keyboard.is_pressed('4'):
        ser.write(b'4')
        time.sleep(0.1) 
        print("Sent '4' command to turn the second servo left")
    if keyboard.is_pressed('5'):
        ser.write(b'5')
        time.sleep(0.1) 
        print("Sent '5' command to turn the second servo right")
    if keyboard.is_pressed('1'):
        ser.write(b'1')
        time.sleep(0.1) 
        print("Sent '1' command to turn the second servo left")
    if keyboard.is_pressed('2'):
        ser.write(b'2')
        time.sleep(0.1) 
        print("Sent '2' command to turn the second servo right")
# Close the serial connection
print("Closing serial connection...")
ser.close()

# Check if the serial connection is closed
if not ser.isOpen():
    print("Serial connection closed!")
else:
    print("Failed to close serial connection.")