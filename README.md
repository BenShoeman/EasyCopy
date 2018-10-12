# EasyCopy

EasyCopy takes information from collection guide lists and copies an Excel-friendly version of them to the clipboard. The goal is to mostly automate data entry with minimal need for the user to intervene.

## Building

You can either run easycopy.py in Python 3, or run `make` to create an executable (which requires pyinstaller). Only tested on Windows 10, but should work for most OSes.

## Dependencies

The exe (if on Windows) generated using `make` has no dependencies.

Building EasyCopy and running easycopy.py through Python have the following dependencies:

- Python 3.7 *(Python 3.5-3.6 will likely work too)*
- Python Modules *(install using pip)*:
  - easygui
  - pyperclip
  - unidecode