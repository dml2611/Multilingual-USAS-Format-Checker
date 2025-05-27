import argparse
import pandas as pd
import re
from pathlib import Path

def check_mwe_template_format(filepath: Path, column_name: str = 'mwe_template') -> list:
    df = pd.read_csv(filepath, sep='\t')
    errors = []
    regex1 = re.compile(r"[\wÀ-ÿ',;.@%’\"&*\-+/ŷ]+_[A-Z*]+")
    regex2 = re.compile(r"\{[A-Za-z0-9ŷ*]+(/[A-Za-z0-9*]*)*\}")
    for i, row in enumerate(df[column_name]):
        if pd.isna(row):
            msg = f"Row {i}: missing template"
            print(msg)
            errors.append(msg)
            continue
        for token in str(row).split():
            if not (regex1.fullmatch(token) or regex2.fullmatch(token)):
                msg = f"Row {i}: invalid token -> {token}"
                print(msg)
                errors.append(msg)
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate the MWE template format in a lexicon.')
    parser.add_argument('input_file', type=Path)
    args = parser.parse_args()
    check_mwe_template_format(args.input_file)
