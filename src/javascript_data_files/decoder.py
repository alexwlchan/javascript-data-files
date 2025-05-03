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

    return json.loads(json_string)
