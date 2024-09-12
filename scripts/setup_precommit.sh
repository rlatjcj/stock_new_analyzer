#!/bin/bash
set -e

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate the virtual environment."
    exit 1
fi

# Install tox and pre-commit
pip install -e .[dev]

# Initialize pre-commit
pre-commit install

echo "pre-commit has been successfully set up."
