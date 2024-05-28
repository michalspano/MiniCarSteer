#!/bin/bash

# Check if `VIRTUAL_ENV` is empty; if so, activate the virtual environment
# for the user. It is assumed that the `venv` is placed in the root.
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual env is not activated. Activating it now..."
    source ./venv/bin/activate
    echo "Activated \`${VIRTUAL_ENV}\`"; echo # add new line
fi

# Check if the `pytest` command is installed in the environment. If not, exit
# the script and notify the user to check if all dependencies are insstalled.
if ! command -v pytest &> /dev/null; then
    echo "\`pytest\` is not installed"
    echo "Did you install all the dependencies from \`requirements.txt\`?"
    exit 1
fi

# Run the coverage, generate type `html`, target the `src` directory
pytest --cov=src --cov-config=.coveragerc --cov-report=html:coverage_report

