SHELL := /bin/sh

# testing / cleanup
test:
	PYTHONPATH=src uv run python -W ignore::ResourceWarning -m unittest discover -s tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

# syncrhonization
sync:
	rsync -avz --progress . goingmerry:p/py/ephem/

fetch:
	rsync -avz --progress goingmerry:p/py/ephem/ .

# documentation
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

# deployment
deploy-docs:
	mkdocs build -d /tmp/mkdocs-site
	git fetch origin pages || git checkout --orphan pages
	git checkout pages
	rm -rf ./* || true
	cp -r /tmp/mkdocs-site/* .
	rm -rf /tmp/mkdocs-site .venv
	git add .
	git commit -m "Deploy: $$(date -I)" || echo "No changes to commit"
	git push origin pages
	git checkout -

unset:
	unset UV_PUBLISH_TOKEN && unset UV_CODEBERG_TOKEN

codeberg: unset
	uv publish --publish-url https://codeberg.org/api/packages/sailorfe/pypi/
