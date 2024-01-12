import tkinter as tk
import math
import serial
import time

# Initialize the serial connection
#  ls /dev | grep rfcomm~
#  sudo rfcomm bind 0 00:22:05:00:56:7E or 98:DA:60:07:D9:C7

DEVICE = '/dev/rfcomm1'
BAUD_RATE = 9600
try:
    serial_connection = serial.Serial(DEVICE, BAUD_RATE, timeout=1)
    print(f"Connected to {DEVICE}")
    time.sleep(2)  # Give some time for the connection to stabilize
except Exception as e:
    print(f"Failed to connect to serial device: {e}")
    serial_connection = None

walking_sequence = []

def draw_leg():
    canvas.delete("all")
    # Convert angles to radians for trigonometric calculations for the first leg
    thigh_angle_rad = math.radians(thigh_slider.get() - 90)
    calf_angle_rad = math.radians(calf_slider.get() + thigh_slider.get() - 180)
    foot_angle_rad = math.radians(foot_slider.get() + calf_slider.get() + thigh_slider.get() - 270)

    # Starting points (adjusted for better visibility) for the first leg
    x0, y0 = 250, 200  # Hip joint for the first leg
    thigh_length = 100  # Pixels
    calf_length = 80  # Pixels

    # Calculate the end of thigh for the first leg
    x1 = x0 + thigh_length * math.sin(thigh_angle_rad)
    y1 = y0 + thigh_length * math.cos(thigh_angle_rad)

    # Draw thigh for the first leg
    canvas.create_line(x0, y0, x1, y1, width=10, fill='blue')

    # Calculate the end of calf for the first leg
    x2 = x1 + calf_length * math.sin(calf_angle_rad)
    y2 = y1 + calf_length * math.cos(calf_angle_rad)

    # Draw calf for the first leg
    canvas.create_line(x1, y1, x2, y2, width=8, fill='green')

    # Draw foot (triangle) for the first leg
    foot_size = 30  # Pixels
    canvas.create_polygon(x2, y2, 
                          x2 + foot_size * math.sin(foot_angle_rad + math.pi / 6), 
                          y2 + foot_size * math.cos(foot_angle_rad + math.pi / 6),
                          x2 + foot_size * math.sin(foot_angle_rad - math.pi / 6), 
                          y2 + foot_size * math.cos(foot_angle_rad - math.pi / 6),
                          fill='red')

    # Convert angles to radians for trigonometric calculations for the second leg
    thigh2_angle_rad = math.radians(thigh2_slider.get() - 90)
    # Foot 2's angle is a combination of its own angle and the thigh's angle
    foot2_angle_rad = math.radians(foot2_slider.get() - 90 + thigh2_slider.get() - 90)

    # Starting points for the second leg
    x0_2, y0_2 = 400, 200  # Hip joint for the second leg

    # Adjust the length of thigh for the second leg based on slider value
    thigh2_length = 100 + (calf2_slider.get() / 2)  # 100mm + 1mm for every 2 degrees

    # Calculate the end of thigh for the second leg
    x1_2 = x0_2 + thigh2_length * math.sin(thigh2_angle_rad)
    y1_2 = y0_2 + thigh2_length * math.cos(thigh2_angle_rad)

    # Draw thigh for the second leg
    canvas.create_line(x0_2, y0_2, x1_2, y1_2, width=10, fill='blue')

    # Draw foot (triangle) for the second leg
    foot_size = 30  # Pixels
    canvas.create_polygon(x1_2, y1_2, 
                          x1_2 + foot_size * math.sin(foot2_angle_rad + math.pi / 6), 
                          y1_2 + foot_size * math.cos(foot2_angle_rad + math.pi / 6),
                          x1_2 + foot_size * math.sin(foot2_angle_rad - math.pi / 6), 
                          y1_2 + foot_size * math.cos(foot2_angle_rad - math.pi / 6),
                          fill='red')

def update_angles():
    # Update the angles and redraw both legs
    update_angles_labels()
    draw_leg()

def update_angles_labels():
    # Calculate and display the effective angles for the first leg
    thigh_angle = thigh_slider.get()
    calf_angle = calf_slider.get()
    foot_angle = foot_slider.get()
    thigh_label.config(text=f"Thigh Angle: {thigh_angle}°")
    calf_label.config(text=f"Calf Angle: {thigh_angle + calf_angle - 90}°")
    foot_label.config(text=f"Foot Angle: {thigh_angle + calf_angle + foot_angle - 180}°")

    # Calculate and display the effective angles for the second leg
    thigh2_angle = thigh2_slider.get()
    calf2_angle = calf2_slider.get()
    foot2_angle = foot2_slider.get()
    thigh2_label.config(text=f"Thigh 2 Angle: {thigh2_angle}°")
    calf2_label.config(text=f"Calf 2 Angle: {thigh2_angle + calf2_angle - 90}°")
    foot2_label.config(text=f"Foot 2 Angle: {thigh2_angle + calf2_angle + foot2_angle - 180}°")

def save_angle_to_sequence():
    # Get the current angles for both legs
    thigh_angle = thigh_slider.get()
    calf_angle = calf_slider.get()
    foot_angle = foot_slider.get()

    thigh2_angle = thigh2_slider.get()
    calf2_angle = calf2_slider.get()
    foot2_angle = foot2_slider.get()

    # Append the angles for the first leg (duplicated) and the second leg to the walking sequence
    # The first leg's angles are duplicated to control the identical outer legs
    walking_sequence.append((thigh_angle, calf_angle, foot_angle, thigh_angle, calf_angle, foot_angle, thigh2_angle, calf2_angle, foot2_angle))
    print(f"Saved Angles: Leg 1 - Thigh {thigh_angle}°, Calf {calf_angle}°, Foot {foot_angle}°; Leg 2 - Thigh {thigh2_angle}°, Calf {calf2_angle}°, Foot {foot2_angle}°")


def animate_sequence(index=0):
    if index < len(walking_sequence):
        angles = walking_sequence[index]

        # Update the sliders for all legs
        thigh_slider.set(angles[0])
        calf_slider.set(angles[1])
        foot_slider.set(angles[2])
        thigh2_slider.set(angles[6])
        calf2_slider.set(angles[7])
        foot2_slider.set(angles[8])
        update_angles()

        # Prepare the list of 9 integers in the required order
        servo_positions = [
            angles[7],         # calf2_slider
            angles[6],         # thigh2_slider
            angles[0],         # thigh_slider (left)
            angles[0],         # thigh_slider (right)
            angles[1],         # calf_slider (left)
            angles[1],         # calf_slider (right)
            angles[2],         # foot_slider (right)
            angles[8],         # foot2_slider
            angles[2],         # foot_slider (left)
        ]

        # Send the positions using the established serial connection
        if serial_connection:
            try:
                positions_str = ','.join(map(str, servo_positions))
                serial_connection.write(positions_str.encode('utf-8'))
                print("Sent servo positions: ", positions_str)
            except Exception as e:
                print(f"Failed to send data: {e}")

        root.after(2000, animate_sequence, index + 1)
    else:
        print("Animation complete.")


def print_sequence():
    # Print the entire walking sequence for both legs
    for idx, angles in enumerate(walking_sequence):
        print(f"Step {idx + 1}: Leg 1 - Thigh {angles[0]}°, Calf {angles[1]}°, Foot {angles[2]}°; Leg 2 - Thigh {angles[3]}°, Calf {angles[4]}°, Foot {angles[5]}°")
    
    # Start the animation
    animate_sequence()

def reset_positions():
    thigh_slider.set(90)
    calf_slider.set(90)
    foot_slider.set(90)
    thigh2_slider.set(90)
    calf2_slider.set(90)
    foot2_slider.set(90)
    update_angles()

# Create the main window
root = tk.Tk()
root.title("Robotic Leg Control")

# Create and place the sliders for the first leg
thigh_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh', command=lambda x: update_angles())
thigh_slider.set(90)
thigh_slider.pack()

calf_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Calf', command=lambda x: update_angles())
calf_slider.set(90)
calf_slider.pack()

foot_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Foot', command=lambda x: update_angles())
foot_slider.set(90)
foot_slider.pack()

# Create and place the labels for the first leg
thigh_label = tk.Label(root, text="Thigh Angle: 90°")
thigh_label.pack()

calf_label = tk.Label(root, text="Calf Angle: 90°")
calf_label.pack()

foot_label = tk.Label(root, text="Foot Angle: 90°")
foot_label.pack()

# Create and place the sliders for the second leg
thigh2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh 2', command=lambda x: update_angles())
thigh2_slider.set(90)
thigh2_slider.pack()

calf2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Calf 2', command=lambda x: update_angles())
calf2_slider.set(90)
calf2_slider.pack()

foot2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Foot 2', command=lambda x: update_angles())
foot2_slider.set(90)
foot2_slider.pack()

# Create and place the labels for the second leg
thigh2_label = tk.Label(root, text="Thigh 2 Angle: 90°")
thigh2_label.pack()

calf2_label = tk.Label(root, text="Calf 2 Angle: 90°")
calf2_label.pack()

foot2_label = tk.Label(root, text="Foot 2 Angle: 90°")
foot2_label.pack()

# Create a button for saving angles to the sequence
save_button = tk.Button(root, text="Save Angles", command=save_angle_to_sequence)
save_button.pack()

# Create a button for printing the entire sequence
print_seq_button = tk.Button(root, text="Print Sequence", command=print_sequence)
print_seq_button.pack()

# Create a "Reset" button
reset_button = tk.Button(root, text="Reset", command=reset_positions)
reset_button.pack()

# Create a larger canvas for drawing both legs
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack()

# Initial draw
draw_leg()

# Start the GUI loop
root.mainloop()

# At the end of the script, close the serial connection
if serial_connection:
    serial_connection.close()
    print("Closed serial connection")