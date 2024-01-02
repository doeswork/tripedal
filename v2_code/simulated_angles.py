import tkinter as tk
import math

def draw_grid():
    # Draw grid lines
    for i in range(0, 801, 10):
        canvas.create_line(i, 0, i, 500, fill="#ddd")
        canvas.create_line(0, i, 800, i, fill="#ddd")

    # Draw and label X and Y axes
    canvas.create_line(0, 250, 800, 250, fill="black", width=2)  # X-axis
    canvas.create_line(400, 0, 400, 500, fill="black", width=2)  # Y-axis
    canvas.create_text(790, 240, text="X", font=("Arial", 12))
    canvas.create_text(410, 10, text="Y", font=("Arial", 12))

def draw_leg():
    canvas.delete("all")
    draw_grid()
    # Convert angles to radians for trigonometric calculations for the first leg
    thigh_angle_rad = math.radians(thigh_slider.get() - 90)
    calf_angle_rad = math.radians(calf_slider.get() + thigh_slider.get() - 225)
    foot_angle_rad = math.radians(foot_slider.get() + calf_slider.get() + thigh_slider.get() - 315)

    # Starting points (adjusted for better visibility) for the first leg
    x0, y0 = 399, 45  # Hip joint for the first leg
    thigh_length = 100  # Pixels
    calf_length = 80  # Pixels

    # Calculate the end of thigh for the first leg
    x1 = x0 + thigh_length * math.sin(thigh_angle_rad)
    y1 = y0 + thigh_length * math.cos(thigh_angle_rad)

    # Draw thigh for the first leg
    canvas.create_line(x0, y0, x1, y1, width=12, fill='blue')

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
    x0_2, y0_2 = 400, 45  # Hip joint for the second leg

    # Adjust the length of thigh for the second leg based on slider value
    thigh2_length = 100 + (calf2_slider.get() / 3)  # 100mm + 1mm for every 3 degrees

    # Calculate the end of thigh for the second leg
    x1_2 = x0_2 + thigh2_length * math.sin(thigh2_angle_rad)
    y1_2 = y0_2 + thigh2_length * math.cos(thigh2_angle_rad)

    # Draw thigh for the second leg
    canvas.create_line(x0_2, y0_2, x1_2, y1_2, width=10, fill='purple')

    # Draw foot (triangle) for the second leg
    foot_size = 30  # Pixels
    canvas.create_polygon(x1_2, y1_2, 
                          x1_2 + foot_size * math.sin(foot2_angle_rad + math.pi / 6), 
                          y1_2 + foot_size * math.cos(foot2_angle_rad + math.pi / 6),
                          x1_2 + foot_size * math.sin(foot2_angle_rad - math.pi / 6), 
                          y1_2 + foot_size * math.cos(foot2_angle_rad - math.pi / 6),
                          fill='red')
def update_angles():
    # Only update angles if flat foot slider is not being used
    if flat_foot_slider.get() == thigh_slider.get():
        update_angles_labels()
        draw_leg()

def update_angles_labels():
    # Calculate and display the effective angles for the first leg
    thigh_angle = thigh_slider.get()
    calf_angle = calf_slider.get()
    foot_angle = foot_slider.get()
    # Update labels with adjusted calf angle calculation
    thigh_label.config(text=f"Thigh Angle: {thigh_angle}°")
    calf_label.config(text=f"Calf Angle: {(thigh_angle + calf_angle - 135) % 360}°")  # Adjusted for new neutral position
    foot_label.config(text=f"Foot Angle: {thigh_angle + calf_angle + foot_angle - 225}°")  # Adjusted foot angle calculation


    # Calculate and display the effective angles for the second leg
    thigh2_angle = thigh2_slider.get()
    calf2_angle = calf2_slider.get()
    foot2_angle = foot2_slider.get()
    thigh2_label.config(text=f"Thigh 2 Angle: {thigh2_angle}°")
    calf2_label.config(text=f"Calf 2 Angle: {thigh2_angle + calf2_angle - 90}°")
    foot2_label.config(text=f"Foot 2 Angle: {thigh2_angle + foot2_angle - 180}°")
    
def update_flat_foot():
    # Get the current thigh angle from the flat foot slider
    thigh_angle = flat_foot_slider.get()
    
    # Update the thigh slider to match the flat foot slider
    thigh_slider.set(thigh_angle)

    # Calculate the required angles to keep the foot flat
    try:
        # Assuming 90 degrees is flat, calculate calf and foot angles
        # Adjusting the calf angle calculation to start from the 135-degree neutral position
        calf_angle = (225 - thigh_angle) % 360  # Adjusted for new neutral position

        foot_angle = 90  # foot always at 90 degrees

        # Check if angles are within the servo range
        if 0 <= calf_angle <= 270 and 0 <= foot_angle <= 180:  # Updated range for calf
            calf_slider.set(calf_angle)
            foot_slider.set(foot_angle)
        else:
            raise ValueError("Impossible to keep foot flat")
    except ValueError as e:
        foot_label.config(text=str(e))

    # Update the angles and redraw the leg
    draw_leg()
    update_angles_labels()

    
# Create the main window
root = tk.Tk()
root.title("Robotic Leg Control")

# Create and place the flat foot slider
flat_foot_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Flat Foot', command=lambda x: update_flat_foot())
flat_foot_slider.set(90)
flat_foot_slider.pack()

# Create and place the sliders for the first leg
thigh_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh', command=lambda x: update_angles())
thigh_slider.set(90)
thigh_slider.pack()

# Modify the range of calf_slider to reflect the new 0-270 degree range
calf_slider = tk.Scale(root, from_=0, to=270, orient='horizontal', label='Calf', command=lambda x: update_angles())
calf_slider.set(135)
calf_slider.pack()

foot_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Foot', command=lambda x: update_angles())
foot_slider.set(90)
foot_slider.pack()

# Create and place the labels for the first leg
thigh_label = tk.Label(root, text="Thigh Angle: 90°")
thigh_label.pack()

calf_label = tk.Label(root, text="Calf Angle: 135°")
calf_label.pack()

foot_label = tk.Label(root, text="Foot Angle: 90°")
foot_label.pack()

# Create and place the sliders for the second leg
thigh2_slider = tk.Scale(root, from_=0, to=180, orient='horizontal', label='Thigh 2', command=lambda x: update_angles())
thigh2_slider.set(90)
thigh2_slider.pack()

calf2_slider = tk.Scale(root, from_=0, to=270, orient='horizontal', label='Calf 2', command=lambda x: update_angles())
calf2_slider.set(0)
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

# Create a larger canvas for drawing both legs
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack()

draw_grid()  # Draw the grid before the leg

draw_leg()

# Start the GUI loop
root.mainloop()
