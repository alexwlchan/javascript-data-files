"""
This file contains pure functions for converting JSON strings
to Python values.

Because I expect some of this JSON to be written by me, and I can
make copy-paste mistakes, there are a couple of ways it tries
to catch errors.
"""

import json
import re
import typing


def decode_from_js(js_string: str, *, varname: str) -> typing.Any:
    """
    Parse a string as a JavaScript value.
    """
    # Matches 'const varname = ' or 'var varname = ' at the start
    # of a string.
    m = re.compile(r"^(?:const |var )?%s = " % varname)

    if not m.match(js_string):
        raise ValueError("Does not start with JavaScript `const` declaration!")

    json_string = m.sub(repl="", string=js_string).rstrip().rstrip(";")

    return decode_from_json(json_string)


def _parse_object_pairs(pairs: list[tuple[str, typing.Any]]) -> dict[str, typing.Any]:
    """
    Convert any object literal into a dict.  This receives a list of
    key-value pairs and returns a dict.

    This is similar to the builtin parser, but it will look for
    duplicate keys and throw a ValueError if they're found; this is
    a protection against me making a copy/paste error in my JavaScript.
    """
    # First try to parse the object as a dictionary; if it's the same
    # length as the pairs, then we know all the keys were unique and
    # we can return.
    pairs_as_dict = dict(pairs)

    if len(pairs_as_dict) == len(pairs):
        return pairs_as_dict

    # Otherwise, let's work out what the duplicate key(s) were, so we
    # can throw an appropriate error message for the user.
    import collections

    key_tally = collections.Counter(k for k, _ in pairs)

    duplicate_keys = [k for k, count in key_tally.items() if count > 1]
    assert len(duplicate_keys) > 0

    if len(duplicate_keys) == 1:
        raise ValueError(f"Found duplicate key in JSON object: {duplicate_keys[0]}")
    else:
        raise ValueError(
            f"Found duplicate keys in JSON object: {', '.join(duplicate_keys)}"
        )


def decode_from_json(json_string: str) -> typing.Any:
    """
    Parse a string as a JSON value.
    """
    return json.loads(json_string, object_pairs_hook=_parse_object_pairs)
