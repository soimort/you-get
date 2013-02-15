SETUP = python3 setup.py

.PHONY: default clean build sdist bdist bdist_egg install release

default: i

i:
	@(cd src/; python -i -c 'import you_get; print("You-Get %s (%s)\n>>> import you_get" % (you_get.__version__, you_get.__date__))')

test:
	$(SETUP) test

clean:
	zenity --question
	rm -fr build/ dist/ src/*.egg-info/
	find . | grep __pycache__ | xargs rm -fr

all: build sdist bdist bdist_egg

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
