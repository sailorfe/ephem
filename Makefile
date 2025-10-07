test:
	PYTHONPATH=src python3 -W ignore::ResourceWarning -m unittest discover -s tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

sync:
	rsync -avz --progress . goingmerry:p/py/ephem/

fetch:
	rsync -avz --progress goingmerry:p/py/ephem/ .

fulldoc:
	pandoc docs/index.md \
    docs/00-installation.md \
    docs/10-getting-started.md \
    docs/20-birth-event-charts.md \
    docs/30-electional-examples.md \
    docs/40-horary-workflows.md \
    docs/50-database-management.md \
    docs/60-advanced-usage.md \
    docs/70-display-config.md \
		--wrap=none \
    -o full-docs.md

pubcb:
	unset UV_PUBLISH_TOKEN
	unset UV_CODEBERG_TOKEN
	uv publish --publish-url https://codeberg.org/api/packages/sailorfe/pypi/

mkd:
	uv venv
	source .venv/bin/activate
	uv pip install mkdocs mkdocs-material
