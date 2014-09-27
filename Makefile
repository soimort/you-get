SETUP = python3 setup.py

.PHONY: default i test clean all html rst build sdist bdist bdist_egg bdist_wheel install rst release

default: i

i:
	@(cd src/; python3 -i -c 'import you_get; print("You-Get %s\n>>> import you_get" % you_get.version.__version__)')

test:
	$(SETUP) test

clean:
	zenity --question
	rm -f README.rst
	rm -fr build/ dist/ src/*.egg-info/
	find . | grep __pycache__ | xargs rm -fr
	find . | grep .pyc | xargs rm -f

all: rst build sdist bdist bdist_egg bdist_wheel

html:
	pandoc README.md > README.html

rst:
	pandoc -s -t rst README.md > README.rst

build:
	$(SETUP) build

sdist:
	$(SETUP) sdist

bdist:
	$(SETUP) bdist

bdist_egg:
	$(SETUP) bdist_egg

bdist_wheel:
	$(SETUP) bdist_wheel

install: bdist_wheel
	$(SETUP) install

release: rst
	zenity --question
	$(SETUP) sdist bdist_wheel upload --sign
