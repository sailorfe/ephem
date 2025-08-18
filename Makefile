test:
	PYTHONPATH=src python3 -W ignore::ResourceWarning -m unittest discover -s tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
