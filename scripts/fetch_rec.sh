#!/bin/bash

# Fetch all the *.rec files from an external resource (GitHub).
# The files are downloaded to the current directory.
BASE_URL="https://github.com/michalspano/dit639-proj-rec-dump/raw/main/car"
BASE_URL_ALT="https://github.com/michalspano/dit639-proj-rec-dump/raw/main/no-GSR"
# ^alternative

# Verify that wget is installed
if ! command -v wget &> /dev/null; then
  echo "\`wget\` could not be found."
  echo "Aborting..."
  exit 1
fi

__fetch_base_rec () {
  for i in {1..5}; do # there's five such files
    name="car${i}.rec"
    printf "Fetching ${name}"
    wget -q "${BASE_URL}${i}.rec"
    echo " OK"
  done
}

__fetch_no_GSR_rec () {
  for i in {1..2}; do # there's two such files
    name="no-GSR-${i}.rec"
    printf "Fetching ${name}"
    wget -q "${BASE_URL_ALT}$-{i}.rec"
    echo " OK"
  done
}

# Detect the `help` flag, show usage.
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
  echo "Usage: fetch_rec.sh [OPTION]"
  echo "Fetch all the *.rec files from an external resource."
  echo "The files are downloaded to the current directory."
  echo "Options:"
  echo "  -a, --all    Fetch all the *.rec files."
  echo "  -h, --help   Display this help and exit."
  exit 0
fi

printf "Fetching *.rec files...\n\n"

__fetch_base_rec # default: fetch "standard" rec files

# If the `--all` flag is provided, the `rec` files with no GSR trace are
# fetched too.
if [ "$1" == "--all" ] || [ "$1" == "-a" ]; then
  printf "\nFetching *.rec files with no GSR trace...\n\n"
  __fetch_no_GSR_rec
fi

echo "Done"

