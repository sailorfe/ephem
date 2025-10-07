#!/usr/bin/env bash
set -e

echo "Building docs..."
uv venv
source .venv/bin/activate
uv pip install mkdocs mkdocs-material
mkdocs build

echo "Deploying to pages branch..."
git checkout pages
rm -rf !(site)  # keep site dir temporarily
cp -r site/* .
rm -rf site .venv
git add .
git commit -m "Deploy: $(date -I)"
git push origin pages
git checkout -
