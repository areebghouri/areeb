# Urdu Dictionary App

This repository contains a simple command line Urdu dictionary application. Multiple dictionaries can be placed in the `dictionaries/` directory as CSV files. Each CSV file must have four comma-separated columns:

1. **Number** – entry number.
2. **Urdu Word** – the word written in Urdu script.
3. **Roman Urdu** – transliteration in Latin script.
4. **Meanings** – four semicolon-separated meanings.

A sample dictionary named `sample.csv` is provided as an example.

## Usage

List available dictionaries:

```bash
python3 dictionary_app.py list
```

Show all entries from a dictionary:

```bash
python3 dictionary_app.py show sample
```

Filter entries by the starting Urdu letter:

```bash
python3 dictionary_app.py show sample --urdu ک
```

Filter entries by the starting Roman letter:

```bash
python3 dictionary_app.py show sample --roman k
```

Add more dictionaries by placing additional CSV files in the `dictionaries/` folder (maximum of 10 is recommended). Name each file with a descriptive name so it can be selected easily.
