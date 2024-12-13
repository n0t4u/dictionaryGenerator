#!/usr/bin/env python3

import argparse
import itertools

def parse_charset(charset):
    """
    Parse the charset argument to return the corresponding characters.
    Supports both predefined charsets and custom input.

    Args:
        charset (str): The charset string (e.g., ?l, ?u, ?d, etc.).

    Returns:
        str: The corresponding characters.
    """
    predefined_charsets = {
        '?l': 'abcdefghijklmnopqrstuvwxyz',  # Lowercase letters
        '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',  # Uppercase letters
        '?d': '0123456789',  # Digits
        '?h': '0123456789abcdef',  # Hexadecimal (lowercase)
        '?H': '0123456789ABCDEF',  # Hexadecimal (uppercase)
        '?s': r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',  # Special characters
        '?a': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' # Alphanumeric + special characters
    }

    # If charset contains predefined set, return corresponding string
    if charset in predefined_charsets:
        return predefined_charsets[charset]

    # Else, return charset as a custom string
    return charset


def extractWords(file, max_length=None, exact_length=None, min_length=None, conditions="", output="extractedWords.txt"):
    """
    Extract words from a dictionary file, filtering based on length and conditions.

    Args:
        file (str): Path to the dictionary file.
        max_length (int, optional): Maximum allowed word length.
        exact_length (int, optional): Exact length of words to include.
        min_length (int, optional): Minimum allowed word length.
        conditions (str, optional): Characters that act as a blacklist.
        output (str): Output file to save the results.

    Returns:
        None: Results are saved to the specified file.
    """
    filtered_words = []
    blacklist = set()

    # Define the predefined blacklists
    predefined_blacklists = {
        '?l': 'abcdefghijklmnopqrstuvwxyz',  # Lowercase letters
        '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',  # Uppercase letters
        '?d': '0123456789',  # Digits
        '?a': 'áéíóúÁÉÍÓÚñÑüÜ',  # Accents
        '?s': r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'  # Special characters
    }

    # Convert conditions into a cumulative blacklist
    if conditions:
        for condition in conditions.split('?'):
            if condition:
                key = '?' + condition  # Recreate the key (e.g., '?s', '?a')
                if key in predefined_blacklists:
                    blacklist.update(predefined_blacklists[key])
                else:
                    blacklist.update(condition)  # Allow custom blacklists

    try:
        with open(file, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip()
                word_length = len(word)

                # Check length conditions
                if ((max_length is not None and word_length > max_length) or
                    (exact_length is not None and word_length != exact_length) or
                    (min_length is not None and word_length < min_length)):
                    continue

                # Check blacklist if conditions are provided
                if blacklist and any(char in blacklist for char in word):
                    continue

                filtered_words.append(word)

        # Save results to the output file in append mode
        with open(output, 'a', encoding='latin-1') as out_file:
            out_file.write("\n".join(filtered_words) + "\n")

        print(f"Extracted words saved to: {output}")

    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def generateDictionary(file, max_length, charset, output="generatedDictionary.txt", prepend=False):
    """
    Generate a new dictionary by padding each word with characters from the charset
    up to the specified length. Optionally prepend the charset instead of appending.
    Args:
        file (str): Path to the dictionary file.
        max_length (int): Maximum length of the generated word.
        charset (str): Characters to pad with.
        output (str): Output file to save the results.
        prepend (bool): Whether to prepend charset to the word instead of appending.
    Returns:
        None: Results are saved to the specified file.
    """
    try:
        # Parse the charset (either predefined or custom)
        charset = parse_charset(charset)

        # Store the generated words
        generated_words = []

        # Read the input dictionary file
        with open(file, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip()
                if len(word) == max_length:
                    # If the word length matches max_length, add it directly
                    generated_words.append(word)
                elif len(word) < max_length:
                    # Calculate how many characters we need to pad to reach max_length
                    padding_length = max_length - len(word)

                    # Generate all combinations of padding
                    for padding in itertools.product(charset, repeat=padding_length):
                        if prepend:
                            new_word = ''.join(padding) + word
                        else:
                            new_word = word + ''.join(padding)
                        generated_words.append(new_word)

        # Save the generated words to the output file in append mode
        with open(output, 'a', encoding='latin-1') as out_file:
            out_file.write("\n".join(generated_words) + "\n")

        print(f"Generated words saved to: {output}")

    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def generateCombinatory(file, output="combinatoryDictionary.txt", extended=False):
    """
    Generate all combinations of uppercase and lowercase letters of a word given a dictionary.
    Optionally include common character substitutions.

    Args:
        file (str): Path to the dictionary file.
        output (str): Output file to save the results.
        extended (bool): Whether to include common character substitutions.

    Returns:
        None: Results are saved to the specified file.
    """
    substitutions = {
        'a': ['4', '@'],
        'b': ['8'],
        'c': ['<', '('],
        'e': ['3'],
        'g': ['6', '9'],
        'i': ['1', '!'],
        'l': ['1', '|'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7', '+'],
        'z': ['2'],
        # Add more substitutions as needed
    }

    try:
        generated_words = []

        with open(file, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip()

                # Generate combinations of uppercase and lowercase
                combos = set(''.join(c) for c in itertools.product(*[(char.lower(), char.upper()) for char in word]))
                generated_words.extend(combos)

                if extended:
                    # Generate combinations with character substitutions
                    for combo in combos:
                        substitutions_combos = set(combo)
                        for char, subs in substitutions.items():
                            if char in combo:
                                for sub in subs:
                                    substitutions_combos.add(combo.replace(char, sub))
                        generated_words.extend(substitutions_combos)

        # Save to the output file
        with open(output, 'a', encoding='latin-1') as out_file:
            out_file.write("\n".join(set(generated_words)) + "\n")

        print(f"Combinatory words saved to: {output}")

    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Create the main parser
    parser = argparse.ArgumentParser(description="Word Generator")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Parser for 'extractWords' function
    extract_parser = subparsers.add_parser(
        'extractWords',
        help="Extract words from a dictionary file.",
        description=(
            "Extract words from a dictionary file while filtering based on length and blacklist conditions.\n"
            "Common blacklist options:\n"
            "  - ?l: Lowercase letters (abcdefghijklmnopqrstuvwxyz).\n"
            "  - ?u: Uppercase letters (ABCDEFGHIJKLMNOPQRSTUVWXYZ).\n"
            "  - ?d: Digits (0123456789).\n"
            "  - ?a: Accents (áéíóúÁÉÍÓÚñÑüÜ).\n"
            "  - ?s: Special characters (!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~).\n"
            "  - Custom: User-defined blacklist."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    extract_parser.add_argument('-f', '--file', type=str, required=True, help="Path to the dictionary file")
    extract_parser.add_argument('-c', '--conditions', type=str, default="", help="Blacklist characters to exclude from the wordlist.")
    extract_parser.add_argument('-o', '--output', type=str, default="extractedWords.txt", help="Output file name.")
    length_group = extract_parser.add_mutually_exclusive_group(required=True)
    length_group.add_argument('-x', '--max-length', type=int, help="Get words with length lower or equal.")
    length_group.add_argument('-e', '--exact-length', type=int, help="Get words with the exact word length.")
    length_group.add_argument('-m', '--min-length', type=int, help="Get words with length greater or equal.")

    # Parser for 'generateDictionary' function
    generate_parser = subparsers.add_parser(
        'generateDictionary',
        help="Generate a new dictionary by padding words.",
        description=(
            "Generate a new dictionary by padding each word with characters from the charset\n"
            "up to the specified length. Optionally prepend the charset instead of appending.\n\n"
            "Available Charsets:\n"
            "  - ?l: Lowercase letters (abcdefghijklmnopqrstuvwxyz).\n"
            "  - ?u: Uppercase letters (ABCDEFGHIJKLMNOPQRSTUVWXYZ).\n"
            "  - ?d: Digits (0123456789).\n"
            "  - ?h: Hexadecimal (0123456789abcdef).\n"
            "  - ?H: Hexadecimal Uppercase (0123456789ABCDEF).\n"
            "  - ?s: Special characters (!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~).\n"
            "  - ?a: Alphanumeric + special characters.\n"
            "  - Custom: User-defined charset."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    generate_parser.add_argument('-f', '--file', type=str, required=True, help="Path to the dictionary file.")
    generate_parser.add_argument('-l', '--max-length', type=int, required=True, help="Maximum allowed word length.")
    generate_parser.add_argument('-c', '--charset', type=str, required=True, help="Characters to pad the words.")
    generate_parser.add_argument('-p', '--prepend', action='store_true', help="Prepend characters instead of appending.")
    generate_parser.add_argument('-o', '--output', type=str, default="generatedDictionary.txt", help="Output file name.")

    # Parser for 'generateCombinatory' function
    combinatory_parser = subparsers.add_parser(
        'generateCombinatory',
        help="Generate combinations of words with different cases and substitutions.",
        description=(
            "Generate all combinations of uppercase and lowercase letters of words from a dictionary.\n"
            "Optionally include common character substitutions for increased coverage.\n"
            "Character substitutions include:\n"
            "  - 'a' -> ['4', '@']\n"
            "  - 'b' -> ['8']\n"
            "  - 'c' -> ['<', '(']\n"
            "  - 'e' -> ['3']\n"
            "  - 'g' -> ['6', '9']\n"
            "  - 'i' -> ['1', '!']\n"
            "  - 'l' -> ['1', '|']\n"
            "  - 'o' -> ['0']\n"
            "  - 's' -> ['5', '$']\n"
            "  - 't' -> ['7', '+']\n"
            "  - 'z' -> ['2']\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    combinatory_parser.add_argument('-f', '--file', type=str, required=True, help="Path to the dictionary file.")
    combinatory_parser.add_argument('-o', '--output', type=str, default="combinatoryDictionary.txt", help="Output file name.")
    combinatory_parser.add_argument('-e', '--extended', action='store_true', help="Include common character substitutions.")

    # Parse the arguments
    args = parser.parse_args()

    if args.command == 'extractWords':
        extractWords(file=args.file, max_length=args.max_length, exact_length=args.exact_length, min_length=args.min_length, conditions=args.conditions, output=args.output)
    elif args.command == 'generateDictionary':
        generateDictionary(file=args.file, max_length=args.max_length, charset=args.charset, prepend=args.prepend, output=args.output)
    elif args.command == 'generateCombinatory':
        generateCombinatory(file=args.file, output=args.output, extended=args.extended)


if __name__ == "__main__":
    main()
