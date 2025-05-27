# 🎯 USAS Lexicon Format Checker - English

This repository provides command-line tools for validating and analyzing the format of English USAS lexicons, including both single-word entries and multi-word expressions (MWEs).

---

## 🧰 Tools

#### 1. `check_column_count.py`
Checks whether each line in a lexicon file contains the expected number of tab-separated columns.

#### 2. `check_duplicates.py`
Identifies duplicate entries in a lexicon file. Supports both single-word and MWE lexicons.

#### 3. `check_mwe_pos_tags.py`
Extracts all unique POS tags from the MWE lexicon. Optionally allows POS tag mapping using a provided JSON file.

#### 4. `check_usas_tags.py`
Validates the USAS tags in both single-word and MWE lexicons against a known tag list.

#### 5. `check_mwe_template_format.py`
Checks for invalid template formats in multiword expressions.

---

## ✅ Requirements
- Python 3.7+

---

## 📌 Usage
Each script is run from the command line. Examples below:

```bash
cd path/to/usas-lexicon-format-checker

# Check for correct column count
python check_column_count.py path/to/singlelexicon.txt 3
python check_column_count.py path/to/mwelexicon.txt 2

# Check for duplicates
python check_duplicates.py path/to/singlelexicon.txt single --output-file dup_single.tsv
python check_duplicates.py path/to/mwelexicon.txt mwe --output-file dup_mwe.tsv

# Extract POS tags from MWE
python check_mwe_pos_tags.py path/to/mwelexicon.txt --output-file pos_tags_mwe.tsv

# Check for valid USAS tags
python check_usas_tags.py --single-file path/to/singlelexicon.txt --mwe-file path/to/mwelexicon.txt --tag-list usas_tagset.txt

# Validate MWE template format
python check_mwe_template_format.py path/to/mwelexicon.txt
```
