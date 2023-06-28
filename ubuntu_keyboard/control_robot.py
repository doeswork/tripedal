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
    if keyboard.is_pressed('w'):
        ser.write(b'w')
        time.sleep(0.1) 
        print("Sent 'w' command to turn the servo left")
    if keyboard.is_pressed('s'):
        ser.write(b's')
        time.sleep(0.1) 
        print("Sent 's' command to turn the servo right")
    if keyboard.is_pressed('e'):
        ser.write(b'e')
        time.sleep(0.1) 
        print("Sent 'e' command to turn the second servo left")
    if keyboard.is_pressed('d'):
        ser.write(b'd')
        time.sleep(0.1) 
        print("Sent 'd' command to turn the second servo right")
    if keyboard.is_pressed('r'):
        ser.write(b'r')
        time.sleep(0.1) 
        print("Sent 'r' command to turn the second servo left")
    if keyboard.is_pressed('f'):
        ser.write(b'f')
        time.sleep(0.1) 
        print("Sent 'f' command to turn the second servo right")
    if keyboard.is_pressed('t'):
        ser.write(b't')
        time.sleep(0.1) 
        print("Sent 't' command to turn the second servo left")
    if keyboard.is_pressed('g'):
        ser.write(b'g')
        time.sleep(0.1) 
        print("Sent 'g' command to turn the second servo right")
    if keyboard.is_pressed('y'):
        ser.write(b'y')
        time.sleep(0.1) 
        print("Sent 'y' command to turn the second servo left")
    if keyboard.is_pressed('h'):
        ser.write(b'h')
        time.sleep(0.1) 
        print("Sent 'h' command to turn the second servo right")
    if keyboard.is_pressed('u'):
        ser.write(b'u')
        time.sleep(0.1) 
        print("Sent 'u' command to turn the second servo left")
    if keyboard.is_pressed('j'):
        ser.write(b'j')
        time.sleep(0.1) 
        print("Sent 'j' command to turn the second servo right")

# Close the serial connection
print("Closing serial connection...")
ser.close()

# Check if the serial connection is closed
if not ser.isOpen():
    print("Serial connection closed!")
else:
    print("Failed to close serial connection.")