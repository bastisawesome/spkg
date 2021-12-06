SOURCES = main.py info.py search.py update.py
OUT_DIR = ~/local/bin
C = pyinstaller
SPEC_PATH = build/
C_ARGS = -F -y --specpath $(SPEC_PATH)

.PHONY: all
all: spkg

spkg:
	$(C) $(C_ARGS) $(SOURCES) -n spkg

install: spkg
	cp dist/spkg $(OUT_DIR)

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf __pycache__

uninstall:
	rm $(OUT_DIR)/spkg
