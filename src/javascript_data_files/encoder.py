"""
This file contains pure functions for converting Python values
to JavaScript strings.

It doesn't do any I/O.
"""

import json
import typing


def encode_as_json(value: typing.Any) -> str:
    """
    Convert a Python value to a JSON-encoded string.
    """
    return json.dumps(value, indent=2)


def encode_as_js(value: typing.Any, varname: str) -> str:
    """
    Convert a Python value to a JSON-encoded JavaScript value.
    """
    json_string = encode_as_json(value)
    js_string = f"const {varname} = {json_string};\n"

    return js_string
