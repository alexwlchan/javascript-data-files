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

    json_string = contents.replace(f"const {varname} = ", "").rstrip().rstrip(";")

    return json.loads(json_string)


def write_js(p: pathlib.Path | str, *, value: typing.Any, varname: str) -> None:
    """
    Write a JavaScript "data file".

    Example:

        >>> red_pentagon = {'sides': 5, 'colour': 'red'}
        >>> write_js('shape.js', value=red_pentagon, varname='redPentagon')
        >>> open('shape.js').read()
        'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'

    """
    json_string = json.dumps(value, indent=2)
    js_string = f"const {varname} = {json_string};\n"

    pathlib.Path(p).parent.mkdir(exist_ok=True, parents=True)

    with open(p, "w") as out_file:
        out_file.write(js_string)
