import pandas as pd
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python print_csv_columns_header.py <path_to_csv_file>")
        return
    file_path = sys.argv[1]
    chunk = pd.read_csv(file_path, nrows=5, header=0)
    print("Columns in CSV file with header=0:")
    print(chunk.columns.tolist())

if __name__ == "__main__":
    main()
