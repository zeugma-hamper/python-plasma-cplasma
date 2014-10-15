
all: test

.PHONY: test

test:
	python setup.py build_ext --inplace
	python test/yamlio_test.py

