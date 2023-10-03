import serial
import time

def send_steps(ser, steps):
    for step in steps:
        step_data = ",".join(map(str, step))
        ser.write((step_data + "\n").encode())
        time.sleep(0.1)  # Add a small delay for reliable data transmission

def main():
    # Initialize the serial connection (replace '/dev/ttyUSB0' with your device)
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    # Some example steps. Replace with your actual step sequence.
    example_steps = [
      [0, -50, 50, 0, 0, 0, 0],
      [-20, 0, 0, -20, 20, 0, 0],
      [0, 0, 0, 0, 0, -20, 0],
      [0, 50, -50, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 10, 0],
      [0, 0, 0, 20, -20, 10, 0],
      [20, 0, 0, 0, 0, 0, 0]
    ]
    
    # Wait for the Arduino to be ready
    time.sleep(2)

    # Sending 'start' to initialize step sequence
    ser.write(b'start\n')
    time.sleep(0.1)
    
    # Sending the step sequences
    send_steps(ser, example_steps)

    # Sending 'run' to execute the steps
    ser.write(b'run\n')
    time.sleep(0.1)

if __name__ == "__main__":
    main()
