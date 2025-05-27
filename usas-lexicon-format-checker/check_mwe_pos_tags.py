import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict

def string_to_path(string_argument: str) -> Path:
    return Path(string_argument).resolve()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract unique POS tags from MWE lexicon.')
    parser.add_argument('input_file', type=string_to_path)
    parser.add_argument('--output-file', type=string_to_path)
    parser.add_argument('--pos-mapper-file', type=string_to_path)
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    pos_mapper_file = args.pos_mapper_file

    pos_tags = set()
    pos_mapping: Dict[str, str] = {}
    if pos_mapper_file:
        with pos_mapper_file.open('r', encoding='utf-8') as pos_mapper_fp:
            pos_mapping = json.load(pos_mapper_fp)

    with input_file.open('r', encoding='utf-8', newline='') as lexicon_data:
        csv_reader = csv.DictReader(lexicon_data, delimiter='\t')

        for row in csv_reader:
            mwe_template = row['mwe_template']
            matches = re.finditer(r'([^_\s]+)_([^_\s}]+)', mwe_template)
            for match in matches:
                pos_tags.add(match.groups()[1])
            matches = re.finditer(r'\{([a-zA-Z*]+)(/[a-zA-Z*]+)*\}', mwe_template)
            for match in matches:
                tags = match.group().strip('{}').split('/')
                for pos_tag in tags:
                    pos_tags.add(pos_tag.strip())

    print('Unique POS Values:')
    if output_file:
        with output_file.open('w', encoding='utf-8', newline='') as write_lexicon_data:
            fieldnames = ['Unique POS Values']
            if pos_mapping:
                fieldnames.append('mapped')
            csv_writer = csv.DictWriter(write_lexicon_data, fieldnames=fieldnames, delimiter='\t')
            csv_writer.writeheader()
            for pos_tag in pos_tags:
                mapped = pos_mapping.get(pos_tag, '')
                print(f'{pos_tag}\t{mapped}')
                csv_writer.writerow({'Unique POS Values': pos_tag, 'mapped': mapped} if mapped else {'Unique POS Values': pos_tag})
    else:
        for pos_tag in pos_tags:
            mapped = pos_mapping.get(pos_tag, '')
            print(f'{pos_tag}\t{mapped}')