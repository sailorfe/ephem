test:
	PYTHONPATH=src python3 -W ignore::ResourceWarning -m unittest discover -s tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

sync:
	rsync -avz --progress . goingmerry:p/py/ephem/

fetch:
	rsync -avz --progress goingmerry:p/py/ephem/ .

fulldoc:
	pandoc -i docs/*.md -o full-docs.md --wrap=none && rsync full-docs.md goingmerry:d/flor/writing/tutorial_ephem.md
