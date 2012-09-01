default: sdist bdist bdist_egg install

clean:
	rm -fr build/ dist/ *.egg-info/

build:
	python3 setup.py build

sdist:
	python3 setup.py sdist

bdist:
	python3 setup.py bdist

bdist_egg:
	python3 setup.py bdist_egg

install: bdist_egg
	sudo python3 setup.py install

release:
	zenity --warning
	python3 setup.py sdist bdist_egg upload

.PHONY: default clean build sdist bdist bdist_egg install release
