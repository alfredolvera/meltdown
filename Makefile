PYTHON ?= python3
CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2

.PHONY: check test-python test-native provenance-check doctor clean

check: test-python test-native provenance-check

test-python:
	$(PYTHON) -m unittest discover -s tests -v

test-native:
	mkdir -p native/build
	$(CC) $(CFLAGS) -Inative/include native/src/memory.c native/tests/test_memory.c -o native/build/test_memory
	./native/build/test_memory

provenance-check:
	$(PYTHON) tools/ki_project.py provenance-check provenance/functions

doctor:
	$(PYTHON) tools/ki_project.py doctor

clean:
	rm -rf native/build

