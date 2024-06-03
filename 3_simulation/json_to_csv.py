import json
import csv
import glob

# Function to adjust knee (calf) angle
def adjust_knee_angle(knee_angle):
    # Convert (-105, 105) to (0, 270)
    return int((knee_angle + 105) * 270 / 210)

def adjust_c2_angle(c2_angle):
    # Convert (0.0, 0.4) to (0, 270)
    return int((c2_angle / 0.4) * 270)

# Function to adjust other angles
def adjust_other_angle(angle):
    # Convert (-90, 90) to (0, 180)
    return int((angle + 90) * 180 / 180)

def convert_json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        # Open the CSV file for writing
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Iterate over each step in the JSON data
            for step_list in data['steps']:
                for step in step_list:
                    row = []
                    for joint, angle in step.items():
                        if joint in ['RK', 'LK']:  # Knee joints
                            adjusted_angle = adjust_knee_angle(angle)
                        elif joint == 'C2':  # C2 joint
                            adjusted_angle = adjust_c2_angle(angle)
                        else:  # Other joints
                            adjusted_angle = adjust_other_angle(angle)
                            adjusted_angle = max(2, min(179, adjusted_angle))

                        # Ensure the result is within the valid range
                        row.append(adjusted_angle)
                    csvwriter.writerow(row)

def adjust_servos(csv_file_path, output_csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    adjusted_rows = []
    for row in rows:
        adjusted_row = [int(value) for value in row]

        # Adjust the left leg servos and C1
        adjusted_row[3] = 180 - adjusted_row[3]  # C1
        adjusted_row[6] = 180 - adjusted_row[6]  # LH
        adjusted_row[7] = 270 - adjusted_row[7]  # LK
        adjusted_row[8] = 180 - adjusted_row[8]  # LF

        # Adjust all feet
        adjusted_row[2] = 180 - adjusted_row[2]  # RF
        adjusted_row[5] = 180 - adjusted_row[5]  # CF
        adjusted_row[8] = 180 - adjusted_row[8]  # LF (already adjusted above, but reiterating for clarity)

        adjusted_rows.append(adjusted_row)

    with open(output_csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(adjusted_rows)

if __name__ == "__main__":
    # Search for JSON files in the current directory
    json_files = glob.glob('*.json')

    if not json_files:
        print("No JSON files found in the current directory.")
    else:
        print("Available JSON files:")
        for idx, file in enumerate(json_files):
            print(f"{idx + 1}. {file}")

        # Let the user select a JSON file
        selection = input("Enter the number of the JSON file you want to use: ")
        try:
            selection_idx = int(selection) - 1
            if 0 <= selection_idx < len(json_files):
                json_file_path = json_files[selection_idx]
                csv_file_path = json_file_path.replace('.json', '.csv')
                adjusted_csv_file_path = csv_file_path.replace('.csv', '_adjusted.csv')

                convert_json_to_csv(json_file_path, csv_file_path)
                adjust_servos(csv_file_path, adjusted_csv_file_path)
                
                print(f"Converted {json_file_path} to {csv_file_path}")
                print(f"Adjusted CSV has been written to {adjusted_csv_file_path}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
