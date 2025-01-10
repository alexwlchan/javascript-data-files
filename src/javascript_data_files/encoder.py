"""
This file contains pure functions for converting Python values
to JavaScript strings.

We prioritise human-readability over absolute efficiency.
For example, JSON is nicely indented to be more readable, rather than
a compact encoding that uses less bytes on disk.
"""

import json
import typing


class HumanReadableEncoder(json.JSONEncoder):
    """
    A custom JSON encoder with a few niceties for human-readability.
    """

    def encode(self, o: typing.Any) -> str:
        """
        Return a JSON string representation of a Python data structure, o.
        """
        if isinstance(o, list) and len(o) < 7 and len(json.dumps(o)) < 60:
            return json.dumps(o)

        return super().encode(o)


def encode_as_json(value: typing.Any) -> str:
    """
    Convert a Python value to a JSON-encoded string.
    """
    return json.dumps(value, indent=2, cls=HumanReadableEncoder)


def encode_as_js(value: typing.Any, varname: str) -> str:
    """
    Convert a Python value to a JSON-encoded JavaScript value.
    """
    json_string = encode_as_json(value)
    js_string = f"const {varname} = {json_string};\n"

    return js_string
