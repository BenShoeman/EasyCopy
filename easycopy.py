# -*- coding: utf8 -*-

import easygui

def main():
    choice = easygui.indexbox(
        "Are you using a guide list with folder-level or box-level info?",
        "Make Selection", ("Folder-Level", "Box-Level"),
        default_choice = "Folder-Level", cancel_choice = "Folder-Level"
    )
    if choice == 0: # Folder-Level
        import copy_folder
        copy_folder.main()
    elif choice == 1: # Box-Level
        import copy_box
        copy_box.main()

if __name__ == "__main__":
    main()