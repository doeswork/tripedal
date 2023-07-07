import bluetooth
import keyboard

# Look for the Bluetooth device
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    print("  {}: {}".format(addr, name))
# 01:23:45:67:92:C9

# You can hardcode the address, e.g., '01:23:45:67:89:AB'
bt_addr = input("Enter the device address: ") 

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bt_addr, 1))

def send_left(event):
    sock.send('l')

def send_right(event):
    sock.send('r')

keyboard.on_press_key("left", send_left)
keyboard.on_press_key("right", send_right)

# Block the program and listen for key presses
keyboard.wait()
