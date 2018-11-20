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
    easygui.msgbox("This is for boxes where each folder has too many items to "
        "enter in the title field. For example, something like the following:",
        "Explanation", image=os.path.join("img", "folderscope_ex.gif")
    )
    json_str = ""
    user_continue = True
    while user_continue:
        text = easygui.codebox(
            "Enter guide list data for 1 box below.",
            "Enter Data",
            (json_str + "\n") if json_str else ""
        )
        if not text or text.strip() == "":
            return
        # Remove potential whitespace at beginning and end
        text = unidecode.unidecode(text.strip())

        # First get settings header if it exists
        json_str = re.findall("^{.*}", text)
        json_str = json_str[0] if json_str else None
        opts = options.get_options(json_str)
        text = re.sub("^{.*}", "", text).strip()

        text = text.replace("Env ", "").replace("Fd ", "").replace("Bk ", "")
        lines = text.split('\n')
        # Get box number, first by trying to find it, then by inputbox if not
        boxnum = re.findall(r'^[\s\n]*\d{1,3}\s+\d', text)
        boxnum = re.findall(r'^[\s\n]*\d{1,3}', boxnum[0]) if boxnum else None
        boxnum = int(boxnum[0].strip()) if boxnum else easygui.integerbox("Enter the box number.", "Enter Box Number", lowerbound=1, upperbound=999)
        # One final check; if user clicked cancel at integerbox, then exit
        if not boxnum:
            return
        else:
            boxnum = str(boxnum)

        entries = []
        last_entry = None
        extras = 0
        for l in lines:
            l = re.sub(r'\s+', " ", l).strip()
            # Perform user substitutions per line
            if opts["user_regex"] is not None and opts["user_subst"] is not None:
                l = opts["user_regex"].sub(opts["user_subst"], l)
            
            if re.match(r'^\d{1,3}(?:\-\d{1,3})?\s', l) and last_entry:
                entries.append(last_entry)
                for _ in range(extras):
                    entries.append(last_entry)
                last_entry = None
                extras = 0
            
            if re.match(r'^\d{1,3}(?:\-\d{1,3})?\s', l):
                while re.match(r'^\d{1,3}(?:\-\d{1,3})?\s', l):
                    # If we have a range, determine the range
                    rng = re.findall(r'^\d{1,3}\-\d{1,3}\s', l)
                    if rng:
                        rng = [int(x) for x in rng[0].strip().split('-')]
                        extras = rng[1] - rng[0]
                    l = re.sub(r'^\d{1,3}(?:\-\d{1,3})?\s', "", l).strip()
                last_entry = l
            else:
                last_entry += "\n" + l
        if last_entry:
            entries.append(last_entry)
            for _ in range(extras):
                entries.append(last_entry)
        
        contents = ""
        for i,e in enumerate(entries, start=1):
            e = e.strip() # Remove unnecessary leading/trailing space
            contents += "folder\t"
            contents += "Folder " + str(i)
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
            contents += "\t" + boxnum + "\tfolder\t" + str(i) + "\t"
            contents += '"' + e.replace('"', '""') + '"'
            contents += "\n"
        
        pyperclip.copy(contents[:-1])

        user_continue = easygui.ynbox("Copied to clipboard.\n\nEnter another box?", "Continue?")
        
if __name__ == "__main__":
    main()