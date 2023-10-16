import csv
import time
import serial

# Steps are declared as global variables
STEPS_COUNT = 7
steps = [
    [0, -15, 15, -10, 10, 0, 0],
    [0, 0, 0, 0, 0, 0, -180],
    [-40, 0, 0, 0, 0, 0, 0],
    [0, -25, 25, -10, 10, 20, 0],
    [40, 0, 0, 0, 0, -20, 0],
    [0, 0, 0, 0, 0, 0, 180],
    [0, 40, -40, 20, -20, 0, 0]
]

# Function to save data to CSV
def save_to_csv(data, filename="robot_walk_data.csv"):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Function to send walking sequence to Arduino
def send_walking_sequence(s):
    data_str = f"{STEPS_COUNT}"
    for step in steps:
        step_str = ",".join(map(str, step))
        data_str += f",{step_str}"
    data_str += "\n"
    print(f"Sending data: {data_str}")  # Debug print
    s.write(data_str.encode('utf-8'))  # Convert the string to bytes

def record_data_and_control_robot():
    DEVICE = '/dev/rfcomm0'
    BAUD_RATE = 9600
    try:
        s = serial.Serial(DEVICE, BAUD_RATE)
        print(f"Connected to {DEVICE}")  # Debug print
    except Exception as e:
        print(f"Failed to connect: {e}")  # Debug print
        exit(1)

    while True:
        # Send steps to robot
        send_walking_sequence(s)

        # Start timer
        start_time = time.time()

        # Wait for completion or failure
        result = input("Enter 'g' if the robot completed 3ft, 't' if it tripped but did something interesting, or 'b' if it fell over: ")

        # Stop timer
        elapsed_time = time.time() - start_time

        # Evaluate performance
        performance = 10 if result == 'g' else 1 if result == 't' else 0 if result == 'b' else None

        if performance is not None:
            # Record both the step sequence and performance metric along with time elapsed
            flat_steps = [item for sublist in steps for item in sublist]
            save_to_csv(flat_steps + [performance, elapsed_time])

        cont = input("Continue recording? (y/n): ")
        if cont.lower() != 'y':
            break

    # Close the serial port
    s.close()
    print("Closed serial connection")  # Debug print

if __name__ == "__main__":
    # Add headers to the CSV file
    headers = [f"Servo{i+1}_Step{j+1}" for j in range(7) for i in range(7)]
    save_to_csv(headers + ["Performance", "TimeElapsed"])
    
    # Start recording data and controlling robot
    record_data_and_control_robot()
