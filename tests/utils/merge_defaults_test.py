from src.utils.helpers import merge_defaults
from typing import Dict, Any

defaults = {
    "a" : None,
    "b" : 4,
    "c" : 3,
    "d" : "bruh",
    "e" : {
        "x" : 1,
        "y" : 2
    }
}

def test_null_dict():
    args_0 = None
    output_dict = merge_defaults(args_0, defaults)
    assert output_dict == defaults

def test_empty_dict():
    args_1 = dict()
    output_dict = merge_defaults(args_1, defaults)
    assert output_dict == defaults

def test_partially_populated_dict():
    args_2 = {
        "a" : 1,
        "b" : 2,
    }
    output_dict = merge_defaults(args_2, defaults)
    expected_output = {
        "a" : 1,
        "b" : 2,
        "c" : 3,
        "d" : "bruh",
        "e" : {
            "x" : 1,
            "y" : 2
        }
    }
    assert output_dict == expected_output


def test_partially_populated_dict_with_nested_arg_included():
    args_3 = {
        "a" : 1,
        "b" : 2,
        "e" : {
            "x" : 123
            }
    }
    output_dict = merge_defaults(args_3, defaults)
    expected_output = {
    "a" : 1,
    "b" : 2,
    "c" : 3,
    "d" : "bruh",
        "e" : {
            "x" : 123,
            "y" : 2
        }
    }
    assert output_dict==expected_output

