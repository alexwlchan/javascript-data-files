"""
Tests for ``javascript_data_files.encoder``.
"""

import string

from javascript_data_files.encoder import encode_as_json, encode_as_js


def test_it_pretty_prints_json() -> None:
    """
    JSON strings are pretty-printed with indentation.
    """
    assert (
        encode_as_json({"sides": 5, "colour": "red"})
        == '{\n  "sides": 5,\n  "colour": "red"\n}'
    )


def test_it_sorts_keys() -> None:
    """
    If you pass `sort_keys=True`, it sorts the keys in JSON objects.
    """
    assert (
        encode_as_json({"sides": 5, "colour": "red"}, sort_keys=False)
        == '{\n  "sides": 5,\n  "colour": "red"\n}'
    )

    assert (
        encode_as_json({"sides": 5, "colour": "red"}, sort_keys=True)
        == '{\n  "colour": "red",\n  "sides": 5\n}'
    )


class TestEnsureAscii:
    """
    Tests for the `ensure_ascii` parameter.
    """

    s = "“hello world”"
    varname = "greeting"

    js_as_utf8 = 'const greeting = "“hello world”";\n'
    js_as_ascii = 'const greeting = "\\u201chello world\\u201d";\n'

    def test_default_is_utf8(self) -> None:
        """
        If you don't pass a value for `ensure_ascii`, then we allow
        UTF-8 in the output.
        """
        assert encode_as_js(self.s, self.varname) == self.js_as_utf8

    def test_explicit_utf8(self) -> None:
        """
        If you pass `ensure_ascii=False`, then we allow UTF-8 in the output.
        """
        assert encode_as_js(self.s, self.varname, ensure_ascii=False) == self.js_as_utf8

    def test_explicit_ascii(self) -> None:
        """
        If you pass `ensure_ascii=True`, then we only return ASCII
        in the output.
        """
        assert encode_as_js(self.s, self.varname, ensure_ascii=True) == self.js_as_ascii


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
