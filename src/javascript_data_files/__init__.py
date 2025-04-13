"""
This is a collection of Python functions for manipulating JavaScript
"data files" -- that is, JavaScript files that define a single variable
with a JSON value.

This is an example of a JavaScript data file:

    const shape = { "sides": 5, "colour": "red" };

Think of this like the JSON module, but for JavaScript files.

"""

import io
import json
import pathlib
import re
import textwrap
import typing
import uuid

from .encoder import encode_as_js, encode_as_json


__version__ = "1.2.1"


T = typing.TypeVar("T")


def read_js(p: pathlib.Path | str, *, varname: str) -> typing.Any:
    """
    Read a JavaScript "data file".

    For example, if you have a file `shape.js` with the following contents:

        const redPentagon = { "sides": 5, "colour": "red" };

    Then you can read it using this function:

        >>> read_js('shape.js', varname='redPentagon')
        {'sides': 5, 'colour': 'red'}

    """
    p = pathlib.Path(p)

    contents = p.read_text()

    m = re.compile(r"^(?:const |var )?%s = " % varname)

    if not m.match(contents):
        raise ValueError(
            f"File {p} does not start with JavaScript `const` declaration!"
        )

    json_string = m.sub(repl="", string=contents).rstrip().rstrip(";")

    return json.loads(json_string)


def read_typed_js[T](p: pathlib.Path | str, *, varname: str, model: type[T]) -> T:
    """
    Read a JavaScript "data file".

    This will validate the contents of the data file against the type
    you provide, and will throw a ``pydantic.ValidationError`` if the
    contents does not match the specified type.
    """
    from .validate_type import validate_type

    data = read_js(p, varname=varname)

    return validate_type(data, model=model)


def write_js(
    p: pathlib.Path | str | io.TextIOBase | io.BufferedIOBase,
    *,
    value: typing.Any,
    varname: str,
) -> None:
    """
    Write a JavaScript "data file".

    You can pass a path-like or file-like object as the first parameter ``p``.

    Example:

        >>> red_pentagon = {'sides': 5, 'colour': 'red'}
        >>> write_js('shape.js', value=red_pentagon, varname='redPentagon')
        >>> open('shape.js').read()
        'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'

    """
    js_string = encode_as_js(value, varname)

    if isinstance(p, io.TextIOBase):
        p.write(js_string)
    elif isinstance(p, io.BufferedIOBase):
        p.write(js_string.encode("utf8"))
    elif isinstance(p, pathlib.Path) or isinstance(p, str):
        p = pathlib.Path(p)

        if p.is_dir():
            raise IsADirectoryError(p)

        p.parent.mkdir(exist_ok=True, parents=True)

        # Write to a temporary file first, then rename this into place.
        #
        # This gives us pseudo-atomic writes -- it's probably not perfect, but
        # it avoids situations where:
        #
        #   * Somebody tries to read the file, and it contains a partial JS string
        #   * The write is interrupted, and the file is left empty
        #
        # Both of which have happened!  Because I often use this running on
        # files on a semi-slow external hard drive, and sometimes things break.
        #
        # The UUID is probably overkill because it would be very unusual for
        # me to have multiple, concurrent writes going on, but it doesn't hurt.
        tmp_p = p.with_suffix(f".{uuid.uuid4()}.js.tmp")

        with tmp_p.open("x") as out_file:
            out_file.write(js_string)

        tmp_p.rename(p)
    else:
        raise TypeError(f"Cannot write JavaScript to {type(p)}!")


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
    p = pathlib.Path(p)
    file_size = p.stat().st_size

    json_to_append = (
        b",\n"
        + textwrap.indent(encode_as_json(value), prefix="  ").encode("utf8")
        + b"\n];\n"
    )

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
    p = pathlib.Path(p)
    file_size = p.stat().st_size

    enc_key = json.dumps(key)
    enc_value = textwrap.indent(encode_as_json(value), prefix="  ").lstrip()

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
