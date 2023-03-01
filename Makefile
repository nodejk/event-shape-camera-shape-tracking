app_src = app
tests_src = tests
all_src = $(app_src) $(tests_src)

test = python3.9 -m unittest discover -s ./tests -p '*Test.py' -v
autoflake = autoflake -r --in-place --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports $(all_src)
mypy_base = mypy --show-error-codes
mypy = $(mypy_base) $(all_src)
black = black $(all_src)

.PHONY: all
all: static test

.PHONY: static
static: mypy

.PHONY: test
test:
	$(test)

.PHONY: mypy
mypy:
	$(mypy)

.PHONY: check-format
check-format:
	$(autoflake) --check
	$(black) --check

.PHONY: format
format:
	$(autoflake)
	$(black)

.PHONY: clean
clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name .coverage`
	rm -f `find . -type f -name ".coverage.*"`
	rm -rf `find . -name __pycache__`
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name htmlcov`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name build`
	rm -rf `find . -type d -name dist`
