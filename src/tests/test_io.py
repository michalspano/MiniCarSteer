"""
Project: DIT639 Project
File: src/tests/test_io.py
Authors: Arumeel Kaisa, Khodaparast Omid, Spano Michal, Säfström Alexander
Description: A set of unit tests for the utility functions that deal with IO.
"""

import pytest
from os import path, remove
from tools.utils import write_log_row, reset_graph_data

### TEST:write_log_row ###

@pytest.fixture
def log_file(tmpdir):
    log_path = tmpdir.join("graph_gen_log.csv")
    yield log_path

    # Teardown: Remove the temporary log file after the test
    if path.exists(log_path):
        remove(log_path)


def test_reset_graph_data(log_file, capsys):
    # No file initially
    assert not path.exists(log_file)

    # When resetting the graph data
    reset_graph_data(path=log_file)

    # Then ensure the log file is reset
    assert path.exists(log_file)

    with open(log_file, "r") as f:
        lines = f.readlines()
        assert len(lines)       == 1
        assert lines[0].strip() == "timestamp;ground;predicted"

    # Check if the function prints the correct message when verbose is True
    captured = capsys.readouterr()
    assert captured.out.strip() == f"> The file {log_file} has been reset."


### TEST:reset_graph_data ###


def test_reset_graph_data_multiple(log_file):
    # Reset multiple consecutive times
    for _ in range(5):
        reset_graph_data(path=log_file)

    assert path.exists(log_file)
    
    # Inspect the file
    with open(log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1 # should NOT append lines (not accumulative)


def test_write_log_row_default_path(log_file): # See 23.txt [LLM]
    # Some dummy data
    timestamp = 123123
    ground, predicted = 0.25, 0.28

    # Log them to the CSV file (custom path, we don't want to write to `tmp` in
    # a test)
    write_log_row(timestamp, ground, predicted, path=log_file)

    assert path.exists(log_file)
    
    with open(log_file, "r") as file:
        lines = file.readlines()
        assert len(lines) == 1 # only one entry written at once

        row = lines[0].strip().split(";") # semicolon delimited

        assert int(row[0])   == timestamp
        assert float(row[1]) == ground
        assert float(row[2]) == predicted


# Test multiple consecutive writes
def test_write_log_row_multiple(log_file):
    # Some dummy data
    n_rows = 10
    timestamp = 123128
    ground, predicted = -0.25, -0.28
    
    # Log them to the CSV file (custom path, we don't want to write to `tmp` in
    # a test). Do this multiple times.
    for i in range(n_rows):
        write_log_row(timestamp + i, ground, predicted, path=log_file)

    assert path.exists(log_file)

    with open(log_file, "r") as file:
        lines = file.readlines()
        assert len(lines) == n_rows # Make sure `n_rows` were added

