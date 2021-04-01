LINTER = flake8
DOCFILES = $(shell ls *.py | sed 's/.py/.html/')
COVER_PKG = $(shell pwd)

FORCE:

docs: $(DOCFILES)

%.html: %.py
	pydoc3 -w ./$<
	git add $@

tests: lint unit

unit: FORCE
	nosetests --exe --verbose --with-coverage --cover-package=$(COVER_PKG)

lint: FORCE
	$(LINTER) *.py
