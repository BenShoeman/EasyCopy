all: easycopy.exe

easycopy.exe:
	pyinstaller --noconsole --onefile --icon=ico/easycopy.ico easycopy.py