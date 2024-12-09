# Dictionary Generator
## Description

**Dictionary Generator** is a Python3 utility designed to manipulate and generate wordlists for various purposes, such as dictionary-based attacks, data analysis, or text processing. It includes functionality for extracting words from dictionaries, padding words with specific characters, and generating case and substitution combinations for enhanced coverage.
## Features

- **Extract Words.** Filter and extract words based on length and custom blacklist conditions.
- **Generate Dictionary.** Pad words from an existing wordlist with specific characters to create new words.
- **Generate Combinatory.** Create combinations of uppercase, lowercase, and common character substitutions.

## Requirements
- Python 3.x

## Usage
The script provides three commands: `extractWords`, `generateDictionary`, and `generateCombinatory`. Each command has its specific options and arguments.
### Extract Words
Extracts words from a dictionary file based on length and character conditions.
```bash
python3 dictionaryGenerator.py extractWords -f <INPUT_FILE> [OPTIONS]
```

|Option|Description|Example|
|----|----|----|
|-f, --file|Path to the input dictionary file.|-f wordlist.txt|
|-x, --max-length|Get words with length ≤ max length.|-x 10|
|-e, --exact-length|Get words with exact length.|-e 8|
|-m, --min-length|Get words with length ≥ min length.|-m 5|
|-c, --conditions|Blacklist characters. Supports predefined sets (?l, ?u, ?d, ?s, ?a) or custom characters.|-c ?a?s or -c xyz|
|-o, --output|Output file to save results (default: extractedWords.txt).|-o filtered.txt|

Examples:
- Extract words of exactly 8 characters, excluding words with digits:
`python3 dictionaryGenerator.py extractWords -f wordlist.txt -e 8 -c ?d`
- Extract words ≥5 characters, excluding words with accents and special characters, and save it into a file called min5.txt:
`python3 dictionaryGenerator.py extractWords -f wordlist.txt -m 5 -c ?a?s -o min5.txt`

### Generate Dictionary
Generates a new dictionary by padding words with specified characters to a fixed length.
```bash
python3 dictionaryGenerator.py generateDictionary -f <INPUT_FILE> -l <MAX_LENGTH> -c <CHARSET> [OPTIONS]
```
|Option|Description|Example|
|----|----|----|
|-f, --file|Path to the input dictionary file.|-f wordlist.txt|
|-l, --max-length|Maximum allowed word length.|-l 12|
|-c, --charset|Characters to pad with. Supports predefined sets (?l, ?u, ?d, ?s, ?h, ?H, ?a) or custom characters.|-c ?d or -c xyz|
|-p, --prepend|Prepend padding characters instead of appending.|-p|
|-o, --output|Output file to save results (default: generatedDictionary.txt).|-o padded_words.txt|

Examples:
- Pad words to 12 characters using digits:
`python3 dictionaryGenerator.py generateDictionary -f wordlist.txt -l 12 -c ?d`
- Prepend letters to words up to 10 characters:
`python3 dictionaryGenerator.py generateDictionary -f wordlist.txt -l 10 -c abc -p`

### Generate Combinatory
Creates case combinations and substitutions for words in a dictionary.
```bash
python3 dictionaryGenerator.py generateCombinatory -f <INPUT_FILE> [OPTIONS]
```

|Option|Description|Example|
|----|----|----|
|-f, --file|Path to the input dictionary file.|-f wordlist.txt|
|-o, --output|Output file to save results (default: combinatoryDictionary.txt).|-o combinations.txt|
|-e, --extended|Include common character substitutions (e.g., a -> @, o -> 0).|-e|

Examples:
- Generate all case combinations of words:
`python3 dictionaryGenerator.py generateCombinatory -f wordlist.txt`
- Generate case combinations with substitutions:
`python3 dictionaryGenerator.py generateCombinatory -f wordlist.txt -e`

## Predefined Charsets and Blacklists

| Symbol | Characters           | Charset                                                                                          |
|--------|----------------------|--------------------------------------------------------------------------------------------------|
| ?l     | Lowercase letters    | abcdefghijklmnopqrstuvwxyz                                                                       |
| ?u     | Uppercase letters    | ABCDEFGHIJKLMNOPQRSTUVWXYZ                                                                       |
| ?d     | Digits               | 0123456789                                                                                       |
| ?h     | Hexadecimal          | 0123456789abcdef                                                                                 |
| ?H     | Hexadecimal Uppercase | 0123456789ABCDEF                                                                                 |
| ?s     | Special characters   | !"#$%&'()*+,-./:;<=>?@[\\]^_`{}~&#124;|                                                                   |
| ?a     | Accented letters | áéíóúÁÉÍÓÚñÑüÜ                                                                                   |
| ?a     | Alphanumeric + special characters | abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~&#124;|

## Advisory
This tool has been created progressively with the help of an AI.

## License
This script is provided under the MIT License. Feel free to use and modify it.
