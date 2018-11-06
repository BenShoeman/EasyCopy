# -*- coding: utf8 -*-

import easygui

def main():
    options = ["Folder-Level (Standard)", "Folder-Level (Use S&C for Title)", "Box-Level", "Exit"]

    user_continue = True
    while user_continue:
        choice = easygui.buttonbox(
            "Are you using a guide list with folder-level or box-level info?",
            "Make Selection", options, default_choice = options[0], cancel_choice = None
        )
        if choice == "Folder-Level (Standard)":
            import easycopy.folder
            easycopy.folder.main()
        elif choice == "Folder-Level (Use S&C for Title)":
            import easycopy.folder_snc
            easycopy.folder_snc.main()
        elif choice == "Box-Level":
            import easycopy.box
            easycopy.box.main()
        
        if choice is None or choice == "Exit": user_continue = False

if __name__ == "__main__":
    main()