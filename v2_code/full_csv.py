import os
import pandas as pd

def list_csv_files():
    # List all files in the current directory
    files = os.listdir('.')
    # Filter out files that are not CSV
    csv_files = [file for file in files if file.endswith('.csv')]
    return csv_files

def convert_floats_to_ints(df):
    # Convert all float columns to ints (assuming no NaNs and it's safe to convert)
    float_cols = df.select_dtypes(include=['float']).columns
    for col in float_cols:
        df[col] = df[col].astype(int)
    return df

def main():
    csv_files = list_csv_files()

    # Print the list of CSV files with a number for each
    for i, file in enumerate(csv_files, 1):
        print(f"{i}: {file}")

    # Prompt the user to choose a file
    file_number = int(input("Enter the number of the CSV file you want to open: "))
    selected_file = csv_files[file_number - 1]

    # Load the DataFrame
    df = pd.read_csv(selected_file)

    # Convert floats to ints
    df = convert_floats_to_ints(df)

    # Print the DataFrame
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(selected_file, index=False)
    print(f"The file '{selected_file}' has been updated with integers.")

if __name__ == "__main__":
    main()

