default: install sdist bdist

clean:
	rm -fr build/ dist/

build:
	python3 setup.py build

install: build
	sudo python3 setup.py install

sdist:
	python3 setup.py sdist

bdist:
	python3 setup.py bdist

.PHONY: default clean build install sdist bdist
