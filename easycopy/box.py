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

import easycopy.options as options

def main():
    text = easygui.codebox("Enter the box-level inventory below.", "Enter Data")
    if not text or text.strip() == "":
        return
    # Remove potential whitespace at beginning and end
    text = unidecode.unidecode(text.strip())

    # First get settings header if it exists
    json_str = re.findall("^{.*}", text)
    json_str = json_str[0] if json_str else None
    opts = options.get_options(json_str)
    text = re.sub("^{.*}", "", text).strip()

    lines = text.split('\n')
    # Get first box number, first by trying to find it, then by inputbox if not
    first_num = re.findall(r'^[\s\n]*\d{1,3}', text)
    first_num = int(first_num[0].strip()) if first_num else easygui.integerbox("Enter the box number.", "Enter Box Number", lowerbound=1, upperbound=999)
    first_num = first_num if first_num else 1

    entries = []
    last_entry = None
    extras = 0
    for l in lines:
        l = re.sub(r'\s+', " ", l).strip()
        # Perform user substitutions per line
        if opts["user_regex"] is not None and opts["user_subst"] is not None:
            l = opts["user_regex"].sub(opts["user_subst"], l)
        
        if re.match(r'^\d+(?:\-\d+)?\s', l) and last_entry:
            entries.append(last_entry)
            for _ in range(extras):
                entries.append(last_entry)
            last_entry = None
            extras = 0
        
        if re.match(r'^\d+(?:\-\d+)?\s', l):
            while re.match(r'^\d+(?:\-\d+)?\s', l):
                # If we have a range, determine the range
                rng = re.findall(r'^\d+\-\d+\s', l)
                if rng:
                    rng = [int(x) for x in rng[0].strip().split('-')]
                    extras = rng[1] - rng[0]
                l = re.sub(r'^\d+(?:\-\d+)?\s', "", l).strip()
            last_entry = l
        else:
            last_entry += "\n" + l
    if last_entry:
        entries.append(last_entry)
        for _ in range(extras):
            entries.append(last_entry)
    
    contents = ""
    for i,e in enumerate(entries, start=first_num):
        e = e.strip() # Remove unnecessary leading/trailing space
        contents += "box\t"
        contents += "Box " + str(i)
        # Get all years from current entry. The replace business will change a
        # year like '66 to 1966 or '01 to 2001 (19/20 dependent on current year)
        years = [y.replace("'", "19" if int(y[1:]) > datetime.now().year % 100 else "20") if len(y) < 4 else y for y in re.findall(r"(?:[1-2]\d{3}|'\d\d)", e)]
        years = [int(y) for y in years if opts["min_year"] <= int(y) <= datetime.now().year]
        if years:
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
            contents += "\t\t\tn.d."
        contents += "\t" + str(i) + "\tbox\t\t"
        contents += '"' + e.replace('"', '""') + '"'
        contents += "\n"
    
    pyperclip.copy(contents[:-1])
    easygui.msgbox("Copied to clipboard.", "Done")
        
if __name__ == "__main__":
    main()