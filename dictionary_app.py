import os
import csv
import argparse
from typing import List, Dict

DICTIONARY_DIR = os.path.join(os.path.dirname(__file__), "dictionaries")

class DictionaryEntry:
    def __init__(self, number: str, urdu_word: str, roman_word: str, meanings_field: str):
        self.number = number
        self.urdu_word = urdu_word
        self.roman_word = roman_word
        self.meanings = [m.strip() for m in meanings_field.split(';') if m.strip()]

class Dictionary:
    def __init__(self, path: str):
        self.path = path
        self.entries: List[DictionaryEntry] = []
        self._load()

    def _load(self):
        with open(self.path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 4:
                    continue
                entry = DictionaryEntry(row[0], row[1], row[2], row[3])
                self.entries.append(entry)

    def filter_by_urdu_letter(self, letter: str) -> List[DictionaryEntry]:
        return [e for e in self.entries if e.urdu_word.startswith(letter)]

    def filter_by_roman_letter(self, letter: str) -> List[DictionaryEntry]:
        return [e for e in self.entries if e.roman_word.lower().startswith(letter.lower())]

class DictionaryApp:
    def __init__(self):
        self.dictionaries: Dict[str, Dictionary] = {}
        self._discover_dictionaries()

    def _discover_dictionaries(self):
        if not os.path.exists(DICTIONARY_DIR):
            return
        for filename in os.listdir(DICTIONARY_DIR):
            if filename.endswith('.csv'):
                name = os.path.splitext(filename)[0]
                path = os.path.join(DICTIONARY_DIR, filename)
                self.dictionaries[name] = Dictionary(path)

    def list_dictionaries(self):
        return list(self.dictionaries.keys())

    def get_dictionary(self, name: str) -> Dictionary:
        return self.dictionaries.get(name)


def print_entries(entries: List[DictionaryEntry]):
    for e in entries:
        meanings = '; '.join(e.meanings)
        print(f"{e.number}\t{e.urdu_word}\t{e.roman_word}\t{meanings}")


def main():
    parser = argparse.ArgumentParser(description="Urdu Dictionary App")
    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser('list', help='List available dictionaries')

    show_parser = subparsers.add_parser('show', help='Show dictionary entries')
    show_parser.add_argument('name', help='Dictionary name')
    show_parser.add_argument('--urdu', help='Filter by Urdu letter')
    show_parser.add_argument('--roman', help='Filter by Roman letter')

    args = parser.parse_args()

    app = DictionaryApp()

    if args.command == 'list':
        for name in app.list_dictionaries():
            print(name)
    elif args.command == 'show':
        dictionary = app.get_dictionary(args.name)
        if not dictionary:
            print(f"Dictionary '{args.name}' not found.")
            return
        entries = dictionary.entries
        if args.urdu:
            entries = dictionary.filter_by_urdu_letter(args.urdu)
        if args.roman:
            entries = dictionary.filter_by_roman_letter(args.roman)
        print_entries(entries)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
