"""
Project: DIT639 Project
File: src/tests/test_utils.py
Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström
Description: A set of unit tests for the utility functions in the tools.py file.
"""

import pytest
from re import match
from tools import *
from decimal import DivisionByZero

### TEST:is_within_bounds ###

@pytest.mark.parametrize("predicted, actual, error, expected", [
    (10, 10, 0.25, True),   # Predicted value equal to actual value within 25% error
    (9, 10, 0.25, True),    # Predicted value within 25% error range
    (7, 10, 0.25, False),   # Predicted value outside of 25% error range
    (12, 10, 0.1, False),   # Predicted value outside of 10% error range
])
def test_is_within_bounds_positive(predicted, actual, error, expected):
    assert is_within_bounds(predicted, actual, error) == expected


@pytest.mark.parametrize("predicted, actual, error, expected", [
    (-10, -10, 0.25, True),   # Predicted value equal to actual value within 25% error
    (-8, -10, 0.25, True),    # Predicted value within 25% error range
    (-5, -10, 0.25, False),   # Predicted value outside of 25% error range
    (-20, -10, 0.3, False),   # Predicted value outside of 30% error range
])
def test_is_within_bounds_negative(predicted, actual, error, expected):
    assert is_within_bounds(predicted, actual, error) == expected


# Test case for error value out of range
def test_error_out_of_range():
    with pytest.raises(Exception):
        is_within_bounds(10, 10, 1.5)  # Error value greater than 1

    with pytest.raises(Exception):
        is_within_bounds(10, 10, -0.1)  # Error value less than 0


### TEST:compute_percentage ###

def test_compute_percentage():
    assert compute_percentage(5, 5) == 50.00
    assert compute_percentage(2, 8, precision=1) == 20.0 # custom precision
    assert compute_percentage(5, 0) == 100.00
    assert compute_percentage(2.5, 7.5) == 25.00


# Handle zero division
def test_compute_percentage_division_by_zero():
    msg = "Cannot divide by zero."
    with pytest.raises(DivisionByZero, match=msg):
        compute_percentage(0, 0)


# Handle mismatched types
def test_compute_percentage_with_string_input():
    with pytest.raises(TypeError):
        compute_percentage("5", "5")


### TEST:argparser_init ###

def test_argparser_init_mock_argv(monkeypatch):
    monkeypatch.setattr("sys.argv", ["app.py", "--cid", "456", "--verbose"])
    args = argparser_init()
    assert args.cid == 456    # custom
    assert args.name == "img" # default
    assert args.model == "Thor.joblib" # default
    assert args.verbose       # set
    assert not args.gen_graph # default
    assert not args.dev_mode  # default


### TEST:debug_performance ###

def test_debug_performance(capsys):
    debug_performance(10, 12, 80)
    captured = capsys.readouterr()
    output = captured.out
    assert "Predicted groundSteeringRequest: 10\n" in output
    assert "Actual groundSteeringRequest: 12\n" in output
    assert "Turns within OK interval (%) 80\n" in output


### TEST:log_frame ###

def test_log_frame(capsys):
    timestamp, value = 12312312, 0.22
    log_frame(timestamp, value)

    ms_timestamp = timestamp * 1000000
    captured = capsys.readouterr()
    output = captured.out

    assert "group_9" in output
    assert str(value) in output
    assert str(ms_timestamp) in output

    # Assert that this format is followed
    # group_{GROUP_NR};timestamp_ms;value
    # Use a regex to match the pattern. The group number can be any number between 1-100.
    # The other integers are arbitrary. [See LLM discussion 11.txt]
    assert match(r"group_(?:[1-9]|[1-9][0-9]|100);\d+;\d+", output) is not None

    # Compare the whole string
    assert f"group_{9};{ms_timestamp};{value}" in output


### TEST:format_data_as_string ###

def test_format_data_as_string():
    # Some dummy keyword args
    kwargs = {
        "Magnetic_field_Z": 123,
        "Magnetic_field_Y": 312,
        "Magnetic_field_X": 99
    }

    formatted_text = format_data_as_string(**kwargs)

    expected_text = (
        "Magnetic field Z: 123\n"
        "Magnetic field Y: 312\n"
        "Magnetic field X: 99\n"
        "\n"
    )
    # Strict comparison
    assert formatted_text == expected_text
