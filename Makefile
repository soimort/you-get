.PHONY: default i test clean all html rst build install release

default: i

i:
	@(cd src; python -i -c 'import you_get; print("You-Get %s\n>>> import you_get" % you_get.version.__version__)')

test:
	(cd src; python -m unittest discover -s ../tests)

clean:
	zenity --question
	rm -fr build/ dist/ src/*.egg-info/
	find . | grep __pycache__ | xargs rm -fr
	find . | grep .pyc | xargs rm -f

all: build

html:
	pandoc README.md > README.html

rst:
	pandoc -s -t rst README.md > README.rst

build:
	python -m build

install:
	python -m pip install .

release: build
	@echo 'Upload new version to PyPI using:'
	@echo '	twine upload --sign dist/you_get-VERSION*'
