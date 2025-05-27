import argparse
import pandas as pd
import re
from pathlib import Path

def load_usas_tag_list(filepath: Path) -> list:
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def tag_is_valid(tag: str, base_tags: list) -> bool:
    return any(tag.startswith(base) for base in base_tags)

def check_usas_tags(df: pd.DataFrame, base_tags: list[str], lex_type: str, file_label: str) -> None:
    semantic_tags = df['semantic_tags']
    errors_found = False
    for i, tag_str in enumerate(semantic_tags):
        if not isinstance(tag_str, str):
            print(f'Line {i} missing tag, existing tag is {tag_str}')
            errors_found = True
            continue

        tags = re.split(r' |/', tag_str)
        for tag in tags:
            if not tag:
                print(f'Tag not found in line {i}\n')
                errors_found = True
                continue

            if tag == 'Z99':
                print(f'Not a valid tag Z99 in line {i}\n{df.iloc[i]}\n')
                errors_found = True
                continue

            if not tag[0].isalpha():
                print(f'Not a valid USAS tag {tag} in line {i}\n{df.iloc[i]}\n')
                errors_found = True
            elif tag[0].islower():
                print(f'Not a USAS tag (starts with lowercase) in line {i}: {tag}')
                errors_found = True
            elif tag.isalpha() and tag.isupper():
                print(f'Not a valid USAS tag (all caps) {tag} in line {i}\n{df.iloc[i]}\n')
                errors_found = True
            elif not tag_is_valid(tag, base_tags):
                print(f'Unknown tag {tag} in line {i} of {file_label}\n{df.iloc[i]}\n')
                errors_found = True

    if not errors_found:
        print(f"✅ No issues found in {file_label}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check USAS tag formatting in single and MWE lexicons.')
    parser.add_argument('--single-file', type=Path, help='Path to single word lexicon (TSV)')
    parser.add_argument('--mwe-file', type=Path, help='Path to MWE lexicon (TSV)')
    parser.add_argument('--tag-list', type=Path, required=True, help='Text file with valid USAS base tags (one per line)')
    args = parser.parse_args()

    usas_base_tags = load_usas_tag_list(args.tag_list)

    if args.single_file:
        single_df = pd.read_csv(args.single_file, sep='\t')
        print(f'\n--- Checking USAS tags in single word lexicon: {args.single_file.name} ---\n')
        check_usas_tags(single_df, usas_base_tags, 'single', args.single_file.name)

    if args.mwe_file:
        mwe_df = pd.read_csv(args.mwe_file, sep='\t')
        print(f'\n--- Checking USAS tags in MWE lexicon: {args.mwe_file.name} ---\n')
        check_usas_tags(mwe_df, usas_base_tags, 'mwe', args.mwe_file.name)