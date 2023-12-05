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
    
        # Convert angles to radians for trigonometric calculations for the third leg
    thigh3_angle_rad = math.radians(thigh3_slider.get() - 90)
    calf3_angle_rad = math.radians(calf3_slider.get() + thigh3_slider.get() - 180)
    foot3_angle_rad = math.radians(foot3_slider.get() + calf3_slider.get() + thigh3_slider.get() - 270)

    # Starting points for the third leg
    x0_3, y0_3 = 550, 200  # Hip joint for the third leg

    # Calculate the end of thigh for the third leg
    x1_3 = x0_3 + thigh_length * math.sin(thigh3_angle_rad)
    y1_3 = y0_3 + thigh_length * math.cos(thigh3_angle_rad)

    # Draw thigh for the third leg
    canvas.create_line(x0_3, y0_3, x1_3, y1_3, width=10, fill='blue')

    # Calculate the end of calf for the third leg
    x2_3 = x1_3 + calf_length * math.sin(calf3_angle_rad)
    y2_3 = y1_3 + calf_length * math.cos(calf3_angle_rad)

    # Draw calf for the third leg
    canvas.create_line(x1_3, y1_3, x2_3, y2_3, width=8, fill='green')

    # Draw foot (triangle) for the third leg
    canvas.create_polygon(x2_3, y2_3, 
                          x2_3 + foot_size * math.sin(foot3_angle_rad + math.pi / 6), 
                          y2_3 + foot_size * math.cos(foot3_angle_rad + math.pi / 6),
                          x2_3 + foot_size * math.sin(foot3_angle_rad - math.pi / 6), 
                          y2_3 + foot_size * math.cos(foot3_angle_rad - math.pi / 6),
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

    # Calculate and display the effective angles for the third leg
    thigh3_angle = thigh3_slider.get()
    calf3_angle = calf3_slider.get()
    foot3_angle = foot3_slider.get()
    thigh3_label.config(text=f"Thigh 3 Angle: {thigh3_angle}°")
    calf3_label.config(text=f"Calf 3 Angle: {thigh3_angle + calf3_angle - 90}°")
    foot3_label.config(text=f"Foot 3 Angle: {thigh3_angle + calf3_angle + foot3_angle - 180}°")

def save_angle_to_sequence():
    # Get the current angles for all three legs
    thigh_angle = thigh_slider.get()
    calf_angle = calf_slider.get()
    foot_angle = foot_slider.get()

    thigh2_angle = thigh2_slider.get()
    calf2_angle = calf2_slider.get()
    foot2_angle = foot2_slider.get()

    thigh3_angle = thigh3_slider.get()
    calf3_angle = calf3_slider.get()
    foot3_angle = foot3_slider.get()

    # Append the angles for all three legs to the walking sequence
    walking_sequence.append((thigh_angle, calf_angle, foot_angle, 
                             thigh2_angle, calf2_angle, foot2_angle, 
                             thigh3_angle, calf3_angle, foot3_angle))
    print(f"Saved Angles: Leg 1 - Thigh {thigh_angle}°, Calf {calf_angle}°, Foot {foot_angle}°; " +
          f"Leg 2 - Thigh {thigh2_angle}°, Calf {calf2_angle}°, Foot {foot2_angle}°; " +
          f"Leg 3 - Thigh {thigh3_angle}°, Calf {calf3_angle}°, Foot {foot3_angle}°")


def animate_sequence(index=0):
    if index < len(walking_sequence):
        angles = walking_sequence[index]

        # Update the sliders for all legs
        thigh_slider.set(angles[0])
        calf_slider.set(angles[1])
        foot_slider.set(angles[2])
        thigh2_slider.set(angles[3])
        calf2_slider.set(angles[4])
        foot2_slider.set(angles[5])
        thigh3_slider.set(angles[6])
        calf3_slider.set(angles[7])
        foot3_slider.set(angles[8])
        update_angles()

        # Prepare the list of 9 integers in the required order
        # Assuming the order remains the same as before, but including the third leg
        servo_positions = [
            angles[4],  # calf2_slider
            angles[3],  # thigh2_slider
            angles[0],  # thigh_slider (left)
            angles[6],  # thigh_slider (right, now from the third leg)
            angles[1],  # calf_slider (left)
            angles[7],  # calf_slider (right, now from the third leg)
            angles[2],  # foot_slider (right)
            angles[5],  # foot2_slider
            angles[8],  # foot_slider (left, now from the third leg)
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
    # Print the entire walking sequence for all three legs
    for idx, angles in enumerate(walking_sequence):
        print(f"Step {idx + 1}: Leg 1 - Thigh {angles[0]}°, Calf {angles[1]}°, Foot {angles[2]}°; " +
              f"Leg 2 - Thigh {angles[3]}°, Calf {angles[4]}°, Foot {angles[5]}°; " +
              f"Leg 3 - Thigh {angles[6]}°, Calf {angles[7]}°, Foot {angles[8]}°")
    
    # Start the animation
    animate_sequence()

def reset_positions():
    thigh_slider.set(90)
    calf_slider.set(90)
    foot_slider.set(90)
    thigh2_slider.set(90)
    calf2_slider.set(90)
    foot2_slider.set(90)
    thigh3_slider.set(90)
    calf3_slider.set(90)
    foot3_slider.set(90)
    update_angles()

# Create the main window
root = tk.Tk()
root.title("Robotic Leg Control")

# Configure the grid layout
root.grid_columnconfigure(0, weight=1, minsize=400) 
root.grid_columnconfigure(1, weight=1, minsize=400) 
root.grid_columnconfigure(2, weight=1, minsize=400) 

# Create and place the sliders for the first leg
thigh_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh', command=lambda x: update_angles())
thigh_slider.set(90)

calf_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Calf', command=lambda x: update_angles())
calf_slider.set(90)

foot_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Foot', command=lambda x: update_angles())
foot_slider.set(90)

# Create and place the labels for the first leg
thigh_label = tk.Label(root, text="Thigh Angle: 90°")

calf_label = tk.Label(root, text="Calf Angle: 90°")

foot_label = tk.Label(root, text="Foot Angle: 90°")

# Create and place the sliders for the second leg
thigh2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh 2', command=lambda x: update_angles())
thigh2_slider.set(90)

calf2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Calf 2', command=lambda x: update_angles())
calf2_slider.set(90)

foot2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Foot 2', command=lambda x: update_angles())
foot2_slider.set(90)

# Create and place the labels for the second leg
thigh2_label = tk.Label(root, text="Thigh 2 Angle: 90°")

calf2_label = tk.Label(root, text="Calf 2 Angle: 90°")

foot2_label = tk.Label(root, text="Foot 2 Angle: 90°")

# Create and place the sliders for the third leg
thigh3_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh 3', command=lambda x: update_angles())
thigh3_slider.set(90)

calf3_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Calf 3', command=lambda x: update_angles())
calf3_slider.set(90)

foot3_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Foot 3', command=lambda x: update_angles())
foot3_slider.set(90)

# Create and place the labels for the third leg
thigh3_label = tk.Label(root, text="Thigh 3 Angle: 90°")

calf3_label = tk.Label(root, text="Calf 3 Angle: 90°")

foot3_label = tk.Label(root, text="Foot 3 Angle: 90°")

# Create and place the sliders for the first leg
thigh_slider.grid(row=0, column=0)
calf_slider.grid(row=1, column=0)
foot_slider.grid(row=2, column=0)

# Create and place the sliders for the second leg
thigh2_slider.grid(row=0, column=1)
calf2_slider.grid(row=1, column=1)
foot2_slider.grid(row=2, column=1)

# Create and place the sliders for the third leg
thigh3_slider.grid(row=0, column=2)
calf3_slider.grid(row=1, column=2)
foot3_slider.grid(row=2, column=2)

# Create a button for saving angles to the sequence
save_button = tk.Button(root, text="Save Angles", command=save_angle_to_sequence)

# Create a button for printing the entire sequence
print_seq_button = tk.Button(root, text="Print Sequence", command=print_sequence)

# Create a "Reset" button
reset_button = tk.Button(root, text="Reset", command=reset_positions)

# Create a larger canvas for drawing both legs
canvas = tk.Canvas(root, width=800, height=500)

# Sliders for the first leg
thigh_slider.grid(row=0, column=0)
calf_slider.grid(row=1, column=0)
foot_slider.grid(row=2, column=0)

# Labels for the first leg
thigh_label.grid(row=3, column=0)
calf_label.grid(row=4, column=0)
foot_label.grid(row=5, column=0)

# Sliders for the second leg
thigh2_slider.grid(row=0, column=1)
calf2_slider.grid(row=1, column=1)
foot2_slider.grid(row=2, column=1)

# Labels for the second leg
thigh2_label.grid(row=3, column=1)
calf2_label.grid(row=4, column=1)
foot2_label.grid(row=5, column=1)

# Sliders for the third leg
thigh3_slider.grid(row=0, column=2)
calf3_slider.grid(row=1, column=2)
foot3_slider.grid(row=2, column=2)

# Labels for the third leg
thigh3_label.grid(row=3, column=2)
calf3_label.grid(row=4, column=2)
foot3_label.grid(row=5, column=2)

# Buttons
save_button.grid(row=6, column=0, columnspan=3)
print_seq_button.grid(row=7, column=0, columnspan=3)
reset_button.grid(row=8, column=0, columnspan=3)

# Canvas
canvas.grid(row=9, column=0, columnspan=3)

# Initial draw
draw_leg()

# Start the GUI loop
root.mainloop()

# At the end of the script, close the serial connection
if serial_connection:
    serial_connection.close()
    print("Closed serial connection")