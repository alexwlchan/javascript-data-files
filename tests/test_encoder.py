"""
Tests for ``javascript_data_files.encoder``.
"""

import string

from javascript_data_files.encoder import encode_as_json


def test_it_pretty_prints_json() -> None:
    """
    JSON strings are pretty-printed with indentation.
    """
    assert (
        encode_as_json({"sides": 5, "colour": "red"})
        == '{\n  "sides": 5,\n  "colour": "red"\n}'
    )


def test_a_list_of_ints_is_not_split_over_multiple_lines() -> None:
    """
    If there's a list of small integers, they're printed on one line
    rather than across multiple lines.
    """
    assert encode_as_json([1, 2, 3]) == "[1, 2, 3]"


def test_a_list_of_long_ints_is_indented_and_split() -> None:
    """
    If there's a list with more integers than a sensible line length,
    they're split across multiple lines.
    """
    json_string = encode_as_json(list(range(100)))

    assert json_string == (
        "["
        "\n  0,\n  1,\n  2,\n  3,\n  4,\n  5,\n  6,\n  7,\n  8,\n  9,"
        "\n  10,\n  11,\n  12,\n  13,\n  14,\n  15,\n  16,\n  17,\n  18,\n  19,"
        "\n  20,\n  21,\n  22,\n  23,\n  24,\n  25,\n  26,\n  27,\n  28,\n  29,"
        "\n  30,\n  31,\n  32,\n  33,\n  34,\n  35,\n  36,\n  37,\n  38,\n  39,"
        "\n  40,\n  41,\n  42,\n  43,\n  44,\n  45,\n  46,\n  47,\n  48,\n  49,"
        "\n  50,\n  51,\n  52,\n  53,\n  54,\n  55,\n  56,\n  57,\n  58,\n  59,"
        "\n  60,\n  61,\n  62,\n  63,\n  64,\n  65,\n  66,\n  67,\n  68,\n  69,"
        "\n  70,\n  71,\n  72,\n  73,\n  74,\n  75,\n  76,\n  77,\n  78,\n  79,"
        "\n  80,\n  81,\n  82,\n  83,\n  84,\n  85,\n  86,\n  87,\n  88,\n  89,"
        "\n  90,\n  91,\n  92,\n  93,\n  94,\n  95,\n  96,\n  97,\n  98,\n  99"
        "\n]"
    )


def test_a_list_of_strings_is_not_split_over_multiple_lines() -> None:
    """
    If there's a list of small strings, they're printed on one line
    rather than across multiple lines.
    """
    assert encode_as_json(["a", "b", "c"]) == '["a", "b", "c"]'


def test_a_list_of_long_strings_is_indented_and_split() -> None:
    """
    If there's a list with more strings than a sensible line length,
    they're split across multiple lines.
    """
    json_string = encode_as_json(list(string.ascii_lowercase))

    assert json_string == (
        "["
        '\n  "a",\n  "b",\n  "c",\n  "d",\n  "e",\n  "f",\n  "g",\n  "h",'
        '\n  "i",\n  "j",\n  "k",\n  "l",\n  "m",\n  "n",\n  "o",\n  "p",'
        '\n  "q",\n  "r",\n  "s",\n  "t",\n  "u",\n  "v",\n  "w",\n  "x",'
        '\n  "y",\n  "z"'
        "\n]"
    )
