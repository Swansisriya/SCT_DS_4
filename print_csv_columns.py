import pandas as pd
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python print_csv_columns.py <path_to_csv_file>")
        return
    file_path = sys.argv[1]
    chunk = pd.read_csv(file_path, nrows=5)
    print("Columns in CSV file:")
    print(chunk.columns.tolist())

if __name__ == "__main__":
    main()
