import json
import pathlib
import typing


__version__ = "1.0.0"


def read_js(p: pathlib.Path | str, *, varname: str) -> typing.Any:
    """
    Read a JavaScript "data file".

    For example, if you have a file `shape.js` with the following contents:

        const redPentagon = { "sides": 5, "colour": "red" };

    Then you can read it using this function:

        >>> read_js('shape.js', varname='redPentagon')
        {'sides': 5, 'colour': 'red'}

    """
    with open(p) as in_file:
        contents = in_file.read()

    if not contents.startswith(f"const {varname} = "):
        raise ValueError(
            f"File {p} does not start with JavaScript `const` declaration!"
        )

    if not contents.rstrip().endswith(";"):
        raise ValueError(f"File {p} does not end with a trailing semicolon!")

    json_string = contents.replace(f"const {varname} = ", "").rstrip().rstrip(";")

    return json.loads(json_string)
