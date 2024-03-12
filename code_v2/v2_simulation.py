import tkinter as tk
import math
import glob
import os
import csv

global distance_to_ground1, distance_to_ground2
global selected_row_index
selected_row_index = None  # Initially, no row is selected

def list_csv_files():
    path = './'  # Current directory
    return glob.glob(os.path.join(path, '*.csv'))  # List all .csv files

def update_csv_selection(option):
    global selected_csv_file
    selected_csv_file.set(option)
    update_csv_positions_list()

def update_csv_positions_list():
    selected_file = selected_csv_file.get()
    if selected_file:
        with open(selected_file, 'r') as file:
            reader = csv.reader(file)
            positions_list.delete(0, tk.END)  # Clear previous list
            for row in reader:
                positions_list.insert(tk.END, row)

def update_sliders_from_row(event):
    global selected_row_index
    selected_row_index = positions_list.curselection()[0]  # Get index of selected row
    selected_row_values = positions_list.get(selected_row_index)  # Get values of selected row
    # Update sliders with the first 6 values from the selected row
    thigh_slider.set(int(selected_row_values[0]))
    calf_slider.set(int(selected_row_values[1]))
    foot_slider.set(int(selected_row_values[2]))
    thigh2_slider.set(int(selected_row_values[3]))
    calf2_slider.set(int(selected_row_values[4]))
    foot2_slider.set(int(selected_row_values[5]))

def delete_selected_row():
    selected_row = positions_list.curselection()
    if selected_row:
        selected_row_index = int(selected_row[0])
        with open(selected_csv_file.get(), 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open(selected_csv_file.get(), 'w', newline='') as file:
            writer = csv.writer(file)
            for idx, row in enumerate(rows):
                if idx != selected_row_index:
                    writer.writerow(row)
                    
# List of CSV files
csv_files = list_csv_files()

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
    global distance_to_ground1, distance_to_ground2
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
    
    foot_triangle_points = [
        (x2, y2), 
        (x2 + foot_size * math.sin(foot_angle_rad + math.pi / 6), y2 + foot_size * math.cos(foot_angle_rad + math.pi / 6)),
        (x2 + foot_size * math.sin(foot_angle_rad - math.pi / 6), y2 + foot_size * math.cos(foot_angle_rad - math.pi / 6))
    ]
    canvas.create_polygon(foot_triangle_points, fill='red')

    foot_bottom_y1 = min(point[1] for point in foot_triangle_points)
    distance_to_ground1 = 225 - foot_bottom_y1
    
    
    
    # Convert angles to radians for trigonometric calculations for the second leg
    thigh2_angle_rad = math.radians(thigh2_slider.get() - 90)
    # Foot 2's angle is a combination of its own angle and the thigh's angle
    foot2_angle_rad = math.radians(foot2_slider.get() - 90 + thigh2_slider.get() - 90)

    # Starting points for the second leg
    x0_2, y0_2 = 400, 45  # Hip joint for the second leg

    # Adjust the length of thigh for the second leg based on slider value
    thigh2_length = 140 + (calf2_slider.get() / 3)  # 100mm + 1mm for every 3 degrees

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
    
    foot2_triangle_points = [
        (x1_2, y1_2), 
        (x1_2 + foot_size * math.sin(foot2_angle_rad + math.pi / 6), y1_2 + foot_size * math.cos(foot2_angle_rad + math.pi / 6)),
        (x1_2 + foot_size * math.sin(foot2_angle_rad - math.pi / 6), y1_2 + foot_size * math.cos(foot2_angle_rad - math.pi / 6))
    ]
    canvas.create_polygon(foot2_triangle_points, fill='red')

    foot2_bottom_y2 = min(point[1] for point in foot2_triangle_points)
    distance_to_ground2 = 225 - foot2_bottom_y2

    # Display the distances for both legs
    distance_label.config(text=f"Leg 1 Distance to Ground: {distance_to_ground1:.2f} pixels, Leg 2 Distance to Ground: {distance_to_ground2:.2f} pixels")
    
def update_angles():
    # Only update angles if flat foot slider is not being used
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

def update_flat_thigh2(val):
    # Set thigh2 angle to the same as flat_thigh2 angle
    thigh2_angle = int(val)
    thigh2_slider.set(thigh2_angle)

    # Set foot2 angle to the opposite direction
    foot2_angle = 180 - thigh2_angle
    foot2_slider.set(foot2_angle)

    # Redraw the leg with updated angles
    draw_leg()
    update_angles_labels()
    
def make_leg2_level():
    global distance_to_ground1, distance_to_ground2

    # Calculate the required adjustment
    adjustment = 1 if distance_to_ground2 < distance_to_ground1 - 1 else -1 if distance_to_ground2 > distance_to_ground1 + 1 else 0

    if adjustment != 0:
        new_value = flat_thigh2_slider.get() + adjustment

        # Set the new value within the slider's range
        new_value = max(0, min(new_value, 180))
        flat_thigh2_slider.set(new_value)

        # Schedule this function to run again after a short delay
        root.after(100, make_leg2_level)

        # Redraw and recalculate distances
        draw_leg()

def print_joint_angles():
    print("First Leg Angles:")
    print(f"  Thigh Angle: {thigh_slider.get()}°")
    print(f"  Calf Angle: {calf_slider.get()}°")
    print(f"  Foot Angle: {foot_slider.get()}°")
    
    print("Second Leg Angles:")
    print(f"  Thigh 2 Angle: {thigh2_slider.get()}°")
    print(f"  Calf 2 Angle: {calf2_slider.get()}°")
    print(f"  Foot 2 Angle: {foot2_slider.get()}°")

    thigh3_angle = abs(180 - thigh_slider.get())
    calf3_angle = abs(270 - calf_slider.get())
    foot3_angle = abs(180 - foot_slider.get())

    print("Third Leg Angles:")
    print(f"  Thigh Angle: {thigh3_angle}°")
    print(f"  Calf Angle: {calf3_angle}°")
    print(f"  Foot Angle: {foot3_angle}°")

    if selected_row_index is not None:  # Check if a row is selected
        # Get the current angles from the sliders
        new_angles = [
            thigh_slider.get(),
            calf_slider.get(),
            foot_slider.get(),
            thigh2_slider.get(),
            calf2_slider.get(),
            foot2_slider.get(),
            abs(180 - thigh_slider.get()),  # Assuming this is how you calculate the third leg angles
            abs(270 - calf_slider.get()),
            abs(180 - foot_slider.get()),
        ]
        
        # Read the current CSV file content
        with open(selected_csv_file.get(), 'r') as file:
            rows = list(csv.reader(file))
        
        # Replace the selected row with new angles
        rows[selected_row_index] = new_angles
        
        # Write the updated rows back to the CSV file
        with open(selected_csv_file.get(), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        # Update the positions_list ListBox with the new CSV content
        update_csv_positions_list()
    else:
        print("No row selected.")

        if selected_csv_file.get():  # Ensure a file is selected
            with open(selected_csv_file.get(), 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    thigh_slider.get(),
                    calf_slider.get(),
                    foot_slider.get(),
                    thigh2_slider.get(),
                    calf2_slider.get(),
                    foot2_slider.get(),
                    abs(180 - thigh_slider.get()),  # Third leg angles
                    abs(270 - calf_slider.get()),
                    abs(180 - foot_slider.get())
                ])
        print("No CSV file selected!")

def update_flat_foot_calf():
    calf_value = flat_foot_calf_slider.get()

    # Update the calf_slider to match the flat_foot_calf slider
    calf_slider.set(calf_value)

    # Get the current thigh angle
    thigh_angle = thigh_slider.get()

    # Calculate the foot angle required to maintain the foot parallel to the ground
    foot_angle = 90 + 225 - (thigh_angle + calf_value)

    # Ensure the foot_angle is within the allowable range of the foot slider
    foot_angle = max(0, min(foot_angle, 180))

    foot_slider.set(foot_angle)

    draw_leg()
    update_angles_labels()

# Create the main window
root = tk.Tk()
root.title("Robotic Leg Control")

level_button = tk.Button(root, text="Make leg 2 level", command=make_leg2_level)
level_button.pack()

distance_label = tk.Label(root, text="Leg 1 Distance: 0 pixels, Leg 2 Distance: 0 pixels")
distance_label.pack()

# Create and place the button
print_angles_button = tk.Button(root, text="Print Joint Angles", command=print_joint_angles)
print_angles_button.pack()

# Variable to keep track of the selected CSV file
selected_csv_file = tk.StringVar(root)
selected_csv_file.set(csv_files[0] if csv_files else '')
# Create a dropdown menu for CSV file selection
csv_dropdown = tk.OptionMenu(root, selected_csv_file, selected_csv_file.get(), *csv_files, command=update_csv_selection)
csv_dropdown.pack()

# Create a ListBox to display positions from the selected CSV file
positions_list = tk.Listbox(root)
positions_list.pack()
# Bind the update_sliders_from_row function to the <<ListboxSelect>> event
positions_list.bind("<<ListboxSelect>>", update_sliders_from_row)

# Create a button to delete selected row
delete_button = tk.Button(root, text="Delete Selected Row", command=delete_selected_row)
delete_button.pack()

# Create frames for two columns of sliders
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create and place the flat foot slider
flat_foot_slider = tk.Scale(left_frame, from_=0, to=180, orient='horizontal', label='Flat Foot', command=lambda x: update_flat_foot())
flat_foot_slider.set(90)
flat_foot_slider.pack()

# Create and place the sliders for the first leg
thigh_slider = tk.Scale(left_frame, from_=0, to=180, orient='horizontal', label='Thigh', command=lambda x: update_angles())
thigh_slider.set(90)
thigh_slider.pack()

flat_foot_calf_slider = tk.Scale(left_frame, from_=0, to=270, orient='horizontal', label='Flat Foot Calf', command=lambda x: update_flat_foot_calf())
thigh_slider.set(135)
flat_foot_calf_slider.pack()

# Modify the range of calf_slider to reflect the new 0-270 degree range
calf_slider = tk.Scale(left_frame, from_=0, to=270, orient='horizontal', label='Calf', command=lambda x: update_angles())
calf_slider.set(135)
calf_slider.pack()

foot_slider = tk.Scale(left_frame, from_=0, to=180, orient='horizontal', label='Foot', command=lambda x: update_angles())
foot_slider.set(90)
foot_slider.pack()

# Create and place the labels for the first leg
thigh_label = tk.Label(left_frame, text="Thigh Angle: 90°")
thigh_label.pack()

calf_label = tk.Label(left_frame, text="Calf Angle: 135°")
calf_label.pack()

foot_label = tk.Label(left_frame, text="Foot Angle: 90°")
foot_label.pack()

flat_thigh2_slider = tk.Scale(right_frame, from_=0, to=180, orient='horizontal', label='Flat Thigh 2', command=update_flat_thigh2)
flat_thigh2_slider.set(90)
flat_thigh2_slider.pack()

# Create and place the sliders for the second leg
thigh2_slider = tk.Scale(right_frame, from_=0, to=180, orient='horizontal', label='Thigh 2', command=lambda x: update_angles())
thigh2_slider.set(90)
thigh2_slider.pack()

calf2_slider = tk.Scale(right_frame, from_=0, to=270, orient='horizontal', label='Calf 2', command=lambda x: update_angles())
calf2_slider.set(0)
calf2_slider.pack()

foot2_slider = tk.Scale(right_frame, from_=0, to=180, orient='horizontal', label='Foot 2', command=lambda x: update_angles())
foot2_slider.set(90)
foot2_slider.pack()

# Create and place the labels for the second leg
thigh2_label = tk.Label(right_frame, text="Thigh 2 Angle: 90°")
thigh2_label.pack()

calf2_label = tk.Label(right_frame, text="Calf 2 Angle: 90°")
calf2_label.pack()

foot2_label = tk.Label(right_frame, text="Foot 2 Angle: 90°")
foot2_label.pack()

# Create a larger canvas for drawing both legs
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack()

draw_grid()  # Draw the grid before the leg

draw_leg()

# Start the GUI loop
root.mainloop()
