import argparse
import pandas as pd
from pathlib import Path

def check_column_count(filepath: Path, expected_columns: int) -> list:
    df = pd.read_csv(filepath, sep='\t')
    errors = []
    if df.shape[1] != expected_columns:
        msg = f"Expected {expected_columns} columns, found {df.shape[1]} in {filepath}"
        print(msg)
        errors.append(msg)
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check number of columns in a lexicon file.')
    parser.add_argument('input_file', type=Path)
    parser.add_argument('expected_columns', type=int)
    args = parser.parse_args()

    check_column_count(args.input_file, args.expected_columns)