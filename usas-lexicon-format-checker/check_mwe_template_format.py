import argparse
import pandas as pd
import re
from pathlib import Path
import sys

def check_mwe_template_format(filepath: Path, column_name: str = 'mwe_template') -> list:
    df = pd.read_csv(filepath, sep='\t')
    errors = []

    # Regex patterns for valid tokens and templates
    regex_token = re.compile(r"[\wÀ-ÿ',;.@%’\"&*\-+/ŷ]+_[A-Z*]+")
    regex_template = re.compile(r"\{[A-Za-z0-9ŷ*]+(/[A-Za-z0-9*]*)*\}")

    for i, row in df.iterrows():
        val = row[column_name]
        if pd.isna(val):
            msg = f"Row {i}: missing template"
            print(msg)
            errors.append(msg)
            continue

        # Check for leading/trailing or multiple spaces (extra spaces)
        val_str = str(val)
        if val_str != val_str.strip() or "  " in val_str:
            print(f"Extra space in line {i}")
            print(df.loc[[i], [column_name, 'semantic_tags']])
            errors.append(f"Extra space in line {i}")

        # Now check tokens — split on whitespace
        tokens = val_str.split()
        for token in tokens:
            if not (regex_token.fullmatch(token) or regex_template.fullmatch(token)):
                print(f"Not a valid template {token}")
                print(df.loc[[i], [column_name, 'semantic_tags']])
                errors.append(f"Invalid token '{token}' in line {i}")

    if not errors:
        print("✅ No issues found in MWE template formatting.")
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate the MWE template format in a lexicon.')
    parser.add_argument('input_file', type=Path, help='Path to the input TSV file.')
    parser.add_argument('--column', type=str, default='mwe_template',
                        help='Column name containing MWE templates (default: mwe_template)')
    args = parser.parse_args()

    errors = check_mwe_template_format(args.input_file, args.column)
    if errors:
        sys.exit(1)
