import csv
import time
import serial

STEPS_COUNT_sent = False
STEPS_COUNT = 7

# center leg, thigh, thigh, calf, calf, ankle, linear
# steps = [
#     [0, -10, 10, -10, 10, 0, 0],
#     [0, 0, 0, 0, 0, 0, -180],
#     [-40, 0, 0, 0, 0, 0, 0],
#     [0, -30, 30, -15, 15, 20, 0],
#     [40, 0, 0, 0, 0, -20, 0],
#     [0, 0, 0, 0, 0, 0, 160],
#     [0, 40, -40, 25, -25, 20, 0]
# ]
steps = [
    [0, -30, 30, -15, 15, 20, 0],
    [40, 0, 0, 0, 0, -20, 0],
    [0, 0, 0, 0, 0, 0, 180],
    [0, 40, -40, 25, -25, 0, 0],
    [0, -10, 10, -10, 10, 0, 0],
    [0, 0, 0, 0, 0, 0, -180],
    [-40, 0, 0, 0, 0, 0, 0]
]
def save_to_csv(data, filename="robot_walk_data.csv"):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def send_walking_sequence(s, steps):
    if isinstance(steps[0], int):  # if steps is actually a single step
        for value in steps:
            data_str = f"{value}\n"
            print(f"Sending data: {data_str.strip()}")
            s.write(data_str.encode('utf-8'))
            time.sleep(0.15)  # Adding delay between each value
    else:  # if steps is a list of steps
        for step in steps:
            for value in step:
                data_str = f"{value}\n"
                print(f"Sending data: {data_str.strip()}")
                s.write(data_str.encode('utf-8'))
                time.sleep(0.15)  # Adding delay between each value


def record_data_and_control_robot():
    DEVICE = '/dev/rfcomm0'
    BAUD_RATE = 9600
    try:
        s = serial.Serial(DEVICE, BAUD_RATE)
        print(f"Connected to {DEVICE}")
        time.sleep(7)

    except Exception as e:
        print(f"Failed to connect: {e}")
        exit(1)

    while True:
        for current_step in steps:
            send_walking_sequence(s, current_step)
            # Assuming some delay needed between sending sequences
            time.sleep(1)

        start_time = time.time()
        
        result = input("Enter 'g' if the robot completed 3ft, 't' if it tripped but did something interesting, or 'b' if it fell over: ")
        
        elapsed_time = time.time() - start_time

        performance = 10 if result == 'g' else 1 if result == 't' else 0 if result == 'b' else None

        if performance is not None:
            flat_steps = [item for sublist in steps for item in sublist]
            save_to_csv(flat_steps + [performance, elapsed_time])

        cont = input("Continue recording? (y/n): ")
        if cont.lower() != 'y':
            break

    s.close()
    print("Closed serial connection")


if __name__ == "__main__":
    record_data_and_control_robot()
