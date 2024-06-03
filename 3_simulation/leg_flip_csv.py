import csv

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
    # Specify the input CSV file and the output CSV file
    input_csv_file = 'walking_sequence.csv'
    output_csv_file = 'adjusted_csv_file.csv'
    
    adjust_servos(input_csv_file, output_csv_file)
    print(f"Adjusted CSV has been written to {output_csv_file}")
