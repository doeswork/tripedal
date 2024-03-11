import csv

def apply_corrections_to_csv(input_csv, output_csv, correction_array):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Convert each row to integers for calculation
            gui_values = [int(value) for value in row]
            # Apply corrections
            corrected_values = [gui + correction for gui, correction in zip(gui_values, correction_array)]
            # Write the corrected values to the output CSV
            writer.writerow(corrected_values)

# Define your correction array based on the example given
correction_array = [-8, 5, 0, 6, 1, 0, -2, 5, 0]

# Example usage
input_csv = 'step_1.csv'  # Your input CSV file with GUI values
output_csv = 'fixed_' + input_csv  # The output file to store corrected values

apply_corrections_to_csv(input_csv, output_csv, correction_array)
