.PHONY: test coverage clean

test:
	PYTHONPATH=test python3 -m unittest discover -s tests

coverage:
	PYTHONPATH=src coverage run -m unittest discover -s tests
	coverage report -m

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f .coverage
	rm -rf htmlcov

