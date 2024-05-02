#!/bin/bash

# Enter src if the user is not already in src
if ! [ "$(basename $(pwd))" = "src" ]; then
    echo "This script must be called \`src\`! Exiting..."
    cd src
else
    echo "\`src\` found"
fi

# Check if `VIRTUAL_ENV` is empty; if so, activate the virtual environment
# for the user.
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual env is not activated. Activating it now..."
    source ../venv/bin/activate
    echo "Activated at ${VIRTUAL_ENV}"
fi

# Check if the `pytest` command is installed in the environment. If not, exit
# the script and notify the user to check if all dependencies are insstalled.
if ! command -v pytest &> /dev/null; then
    echo "\`pytest\` is not installed."
    echo "Did you install all the dependencies from \`requirements.txt\`?"
    exit 1
fi

# Run the coverage, generate type `html`
pytest --cov=. --cov-report html
