# -*- coding: utf8 -*-

import easygui
import os

def read_help(fname):
    options = []
    option_text = {}
    last_option = ""
    last_option_text = ""
    with open(fname) as f:
        for line in f:
            # If we have a header, make that an option
            if len(line) > 2 and line[:2] == "# ":
                if len(last_option) > 0:
                    options.append(last_option.strip())
                    option_text[last_option.strip()] = last_option_text.strip()
                last_option = line[2:]
                last_option_text = ""
            else:
                last_option_text += line
        if len(last_option) > 0:
            options.append(last_option.strip())
            option_text[last_option.strip()] = last_option_text.strip()
    return options, option_text

def main():
    options, option_text = read_help(os.path.join("data", "help.txt"))
    options.append("Back")
    
    user_continue = True
    while user_continue:
        choice = easygui.buttonbox(
            "Select a help option. (Note you can scroll down in the help boxes!)",
            "Make Selection", options, default_choice = options[0], cancel_choice = None
        )
        
        if choice is None or choice == "Back":
            user_continue = False
        else:
            easygui.msgbox(option_text[choice], choice)

if __name__ == "__main__":
    main()