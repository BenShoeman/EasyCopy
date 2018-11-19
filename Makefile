all: easycopy.exe

easycopy.exe:
	pyinstaller --noconsole --onefile --icon=ico/easycopy.ico easycopy.py
	cp -r img dist
	cp -r data dist

clean:
	rm -r build
	rm -r dist
	rm easycopy.spec