import argparse
import csv
from pathlib import Path
from collections import Counter
from typing import Dict

def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for duplicate entries in single or MWE lexicon.')
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('--output-file', type=string_to_path)
    parser.add_argument('file_type', type=str, choices=['single', 'mwe'])
    args = parser.parse_args()

    input_file = args.input_file
    file_type = args.file_type
    output_file = args.output_file

    with input_file.open('r', encoding='utf-8', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')
        duplicate_counter = Counter()
        duplicate_entries: Dict[str, int] = {}
        output_file_field_names = []

        if file_type == 'single':
            for values in csv_reader:
                lemma = values.get('lemma')
                pos_tag = values.get('pos', '')
                duplicate_counter.update([lemma + ' ' + pos_tag])
            print('Lemma (POS Tag): Count')
            for key, count in duplicate_counter.items():
                if count > 1:
                    print(f'{key}: {count}')
                    duplicate_entries[key] = count
            output_file_field_names = ['Lemma (POS Tag)', 'Count']
        else:
            for values in csv_reader:
                mwe_template = values.get('mwe_template')
                duplicate_counter.update([mwe_template])
            print('MWE Template: Count')
            for key, count in duplicate_counter.items():
                if count > 1:
                    print(f'{key}: {count}')
                    duplicate_entries[key] = count
            output_file_field_names = ['MWE Template', 'Count']

        print(f'Total number of duplicate entries: {len(duplicate_entries)}')

        if output_file:
            with output_file.open('w', encoding='utf-8', newline='') as output_fp:
                tsv_writer = csv.DictWriter(output_fp, output_file_field_names, delimiter='\t')
                tsv_writer.writeheader()
                for key, count in duplicate_entries.items():
                    tsv_writer.writerow({output_file_field_names[0]: key,
                                         output_file_field_names[1]: count})