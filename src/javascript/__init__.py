import json
import os
import pathlib
import re
import typing


__version__ = "0.0.1"


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

    m = re.compile(r"^(?:const |var )?%s = " % varname)

    if not m.match(contents):
        raise ValueError(
            f"File {p} does not start with JavaScript `const` declaration!"
        )

    json_string = m.sub(repl="", string=contents).rstrip().rstrip(";")

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


def append_to_js_array(p: pathlib.Path | str, *, value: typing.Any) -> None:
    """
    Append a single value to an array in a JavaScript "data file".

    Example:

        >>> write_js('food.js', value=['apple', 'banana', 'coconut'], varname='fruit')
        >>> append_to_js_array('food.js', value='damson')
        >>> read_js('food.js', varname='fruit')
        ['apple', 'banana', 'coconut', 'damson']

    If you have a large file, this is usually faster than reading,
    appending, and re-writing the entire file.

    """
    file_size = os.stat(p).st_size

    json_to_append = b",\n" + json.dumps(value).encode("utf8") + b"\n];\n"

    with open(p, "rb+") as out_file:
        out_file.seek(file_size - 4)

        if out_file.read(4) == b"\n];\n":
            out_file.seek(file_size - 4)
            out_file.write(json_to_append)
            return

        out_file.seek(file_size - 3)
        if out_file.read(3) in {b"\n];", b"];\n"}:
            out_file.seek(file_size - 3)
            out_file.write(json_to_append)
            return

        out_file.seek(file_size - 2)
        if out_file.read(2) in {b"];", b"]\n"}:
            out_file.seek(file_size - 2)
            out_file.write(json_to_append)
            return

        out_file.seek(file_size - 1)
        if out_file.read(1) == b"]":
            out_file.seek(file_size - 1)
            out_file.write(json_to_append)
            return

        raise ValueError(f"End of file {p!r} does not look like an array")


def append_to_js_object(p: pathlib.Path | str, *, key: str, value: typing.Any) -> None:
    """
    Append a single key/value pair to a JSON object in a JavaScript "data file".

    Example:

        >>> write_js('shape.js', value={'colour': 'red', 'sides': 5}, varname='redPentagon')
        >>> append_to_js_object('shape.js', key='sideLengths', value=[5, 5, 6, 6, 6])
        >>> read_js('shape.js', varname='redPentagon')
        {'colour': 'red', 'sides': 5, 'sideLengths': [5, 5, 6, 6, 6]}

    If you have a large file, this is usually faster than reading,
    appending, and re-writing the entire file.

    """
    file_size = os.stat(p).st_size

    enc_key = json.dumps(key)
    enc_value = json.dumps(value)

    json_to_append = f",\n  {enc_key}: {enc_value}\n}};\n".encode("utf8")

    with open(p, "rb+") as out_file:
        out_file.seek(file_size - 4)

        if out_file.read(4) == b"\n};\n":
            out_file.seek(file_size - 4)
            out_file.write(json_to_append)
            return

        out_file.seek(file_size - 3)
        if out_file.read(3) in {b"\n};", b"};\n"}:
            out_file.seek(file_size - 3)
            out_file.write(json_to_append)
            return

        out_file.seek(file_size - 2)
        if out_file.read(2) in {b"};", b"}\n"}:
            out_file.seek(file_size - 2)
            out_file.write(json_to_append)
            return

        out_file.seek(file_size - 1)
        if out_file.read(1) == b"}":
            out_file.seek(file_size - 1)
            out_file.write(json_to_append)
            return

        raise ValueError(f"End of file {p!r} does not look like an object")
