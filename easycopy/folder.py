# -*- coding: utf8 -*-

from collections import defaultdict
from datetime import datetime
import easygui
import json
import re
import os
import pyperclip
import sys
import unidecode

NUMBER_REGEX = r'^\d+(?:\-\d+)?\s'
ITEM_TYPES = {
    "bk": "Book",
    "bdl": "Bundle",
    "env": "Envelope",
    "fd": "Folder",
    "nbk": "Notebook"
}
ITEM_TYPE_REGEX = r'(' + '|'.join(ITEM_TYPES.keys()) + r')s?'

def main():
    delete_years = easygui.ynbox("Delete the years from each entry when processing guide data?\n\n(MAKE SURE YOU CROSS-REFERENCE WITH THE GUIDE LIST AFTER PASTING!)", "Delete Years?")
    user_continue = True
    while user_continue:
        text = easygui.codebox("Enter guide list data for 1 box below.", "Enter Data")
        if not text or text.strip() == "":
            return # Exit if clicked cancel or nothing inputted
        # Remove potential whitespace at beginning and end
        text = unidecode.unidecode(text.strip())

        # First get settings header if it exists
        opts = re.findall("^{.*}", text)
        if opts:
            opts = defaultdict(lambda: None, json.loads(opts[0]))
            text = re.sub("^{.*}", "", text).strip()
        else:
            opts = defaultdict(lambda: None)
        print(opts)
        min_year = 1600 if opts["min_year"] is None else opts["min_year"]

        text = re.sub(ITEM_TYPE_REGEX + r'\s+(' + NUMBER_REGEX[1:] + ")", "\\2\\1: ", text, flags=re.IGNORECASE)
        # Get box number, first by trying to find it, then by inputbox if not
        boxnum = re.findall(r'^[\s\n]*\d{1,3}\s+\d', text)
        boxnum = re.findall(r'^[\s\n]*\d{1,3}', boxnum[0]) if boxnum else None
        boxnum = int(boxnum[0].strip()) if boxnum else easygui.integerbox("Enter the box number.", "Enter Box Number", lowerbound=1, upperbound=999)
        # One final check; if user clicked cancel at integerbox, then exit
        if not boxnum:
            return
        else:
            boxnum = str(boxnum)
        lines = text.split('\n')
        entries = []
        last_entry = None
        extras = 0
        for l in lines:
            l = re.sub(r'\s+', " ", l).strip()
            
            if re.match(NUMBER_REGEX, l) and last_entry:
                entries.append(last_entry)
                for _ in range(extras):
                    entries.append(last_entry)
                last_entry = None
                extras = 0
            
            if re.match(NUMBER_REGEX, l):
                while re.match(NUMBER_REGEX, l):
                    # If we have a range, determine the range
                    rng = re.findall(r'^\d+\-\d+\s', l)
                    if rng:
                        rng = [int(x) for x in rng[0].strip().split('-')]
                        extras = rng[1] - rng[0]
                    l = re.sub(NUMBER_REGEX, "", l).strip()
                last_entry = l
            else:
                last_entry += " " + l
        if last_entry:
            entries.append(last_entry)
            for _ in range(extras):
                entries.append(last_entry)
        
        contents = ""
        for i,e in enumerate(entries, start=1):
            e = e.strip() # Remove unnecessary leading/trailing space
            file_type = "item" if re.match(ITEM_TYPE_REGEX, e, flags=re.IGNORECASE) else "folder"
            # Replace abbreviations of item types to full length names
            for k,v in ITEM_TYPES.items():
                e = re.sub(k + r':\s', v + ": ", e, flags=re.IGNORECASE)
            # Remove folder piece and set file_type back to folder if Folder: exists
            if "Folder: " in e:
                file_type = "folder"
                e = e.replace("Folder: ", "") # Remove the Folder piece
            contents += file_type + "\t"
            if '"' in e:
                e = '"' + e.replace('"', '""') + '"'
            # Get all years from current entry. The replace business will change a
            # year like '66 to 1966 or '01 to 2001 (19/20 dependent on current year)
            years = [y.replace("'", "19" if int(y[1:]) > datetime.now().year % 100 else "20") if len(y) < 4 else y for y in re.findall(r"(?:[1-2]\d{3}|'\d\d)", e)]
            years = [int(y) for y in years if min_year <= int(y) <= datetime.now().year]
            if years:
                # Remove years we found from entry, including preceding commas/dashes
                # but ONLY if the user wants to delete the years
                if delete_years:
                    contents += re.sub("[,:\-\s]*(?:'\d\d|" + '|'.join(str(y) for y in years) + ')', "", e)
                else:
                    contents += e
                if len(years) >= 2:
                    # Pick the min and max (for out of order years or many years)
                    years = [min(years), max(years)]
                    # If they're the same, just make the second one blank
                    if years[0] == years[1]:
                        years[1] = ""
                if len(years) == 1:
                    # Add a blank entry so we have a tab still
                    years.append("")
                contents += "\t" + "\t".join(str(y) for y in years) + "\t"
            else:
                contents += e
                contents += "\t\t\tn.d."
            contents += "\t" + boxnum + "\t" + file_type + "\t" + str(i)
            contents += "\n"
        
        pyperclip.copy(contents[:-1])

        user_continue = easygui.ynbox("Copied to clipboard.\n\nEnter another box?", "Continue?")
    
if __name__ == "__main__":
    main()