SETUP = python3 setup.py

.PHONY: default clean build sdist bdist bdist_egg install release

default: build sdist bdist bdist_egg

clean:
	zenity --question
	rm -fr build/ dist/ *.egg-info/
	find . | grep __pycache__ | xargs rm -fr

build:
	$(SETUP) build

sdist:
	$(SETUP) sdist

bdist:
	$(SETUP) bdist

bdist_egg:
	$(SETUP) bdist_egg

install: bdist_egg
	sudo $(SETUP) install

release:
	zenity --question
	$(SETUP) sdist bdist_egg upload
