"""
Tests for the ``javascript`` module.
"""

import io
import pathlib
import typing

import pydantic
import pytest

from javascript_data_files import (
    append_to_js_array,
    append_to_js_object,
    read_js,
    read_typed_js,
    write_js,
)


@pytest.fixture
def js_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    Returns a path to a JavaScript file.

    This only returns the path and does not create the file.
    """
    return tmp_path / "data.js"


class TestReadJs:
    """
    Tests for the ``read_js()`` function.
    """

    @pytest.mark.parametrize(
        "text",
        [
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n',
            'var redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n',
            'redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n',
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};',
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n}',
        ],
    )
    def test_can_read_file(self, js_path: pathlib.Path, text: str) -> None:
        """
        JavaScript "data values" can be read from files, with a certain
        amount of allowance for:

        *   whitespace
        *   trailing semicolon or not
        *   a var/const prefix

        """
        js_path.write_text(text)

        assert read_js(js_path, varname="redPentagon") == {"sides": 5, "colour": "red"}

    def test_error_if_path_does_not_exist(self) -> None:
        """
        Reading a file which doesn't exist throws a FileNotFoundError.
        """
        with pytest.raises(FileNotFoundError):
            read_js("doesnotexist.js", varname="shape")

    def test_error_if_path_is_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Reading a path which is a directory throws an IsADirectoryError.
        """
        assert tmp_path.is_dir()

        with pytest.raises(IsADirectoryError):
            read_js(tmp_path, varname="shape")

    def test_non_json_value_is_error(self, js_path: pathlib.Path) -> None:
        """
        Reading a file which doesn't contain a JavaScript "data value"
        throws a ValueError.
        """
        js_path.write_text("const sum = 1 + 1 + 1;")

        with pytest.raises(ValueError):
            read_js(js_path, varname="sum")

    def test_incorrect_varname_is_error(self, js_path: pathlib.Path) -> None:
        """
        Reading a file with the wrong variable name throws a ValueError.
        """
        js_path.write_text(
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

        with pytest.raises(
            ValueError, match="does not start with JavaScript `const` declaration"
        ):
            read_js(js_path, varname="blueTriangle")


class TestReadTypedJs:
    """
    Tests for the ``read_typed_js()`` function.
    """

    def test_matches_model(self, js_path: pathlib.Path) -> None:
        """
        If the data matches the model, it's read correctly.
        """
        js_path.write_text(
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

        Shape = typing.TypedDict("Shape", {"sides": int, "colour": str})

        shape = read_typed_js(js_path, varname="redPentagon", model=Shape)

        assert shape == {"sides": 5, "colour": "red"}

    def test_does_not_match_model(self, js_path: pathlib.Path) -> None:
        """
        If the data does not match the model, it throws a ValidationError.
        """
        js_path.write_text(
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

        Vehicle = typing.TypedDict("Vehicle", {"wheels": int, "colour": str})

        with pytest.raises(pydantic.ValidationError):
            read_typed_js(js_path, varname="redPentagon", model=Vehicle)

    def test_can_read_int(self, js_path: pathlib.Path) -> None:
        """
        It can read typed data which is an int.
        """
        js_path.write_text("const theAnswer = 42;\n")

        answer = read_typed_js(js_path, varname="theAnswer", model=int)
        assert answer == 42

    def test_can_read_list_int(self, js_path: pathlib.Path) -> None:
        """
        It can read typed data which is an int.
        """
        js_path.write_text("const diceValues = [1,2,3,4,5,6];\n")

        answer = read_typed_js(js_path, varname="diceValues", model=list[int])
        assert answer == [1, 2, 3, 4, 5, 6]


class TestWriteJs:
    """
    Tests for the ``write_js()`` function.
    """

    def test_can_write_file(self, js_path: pathlib.Path) -> None:
        """
        Writing to a file stores the correct JavaScript string.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_can_write_to_str(self, tmp_path: pathlib.Path) -> None:
        """
        It can write to a path passed as a ``str``.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        js_path = tmp_path / "shape.js"

        write_js(p=str(js_path), value=red_pentagon, varname="redPentagon")

        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_can_write_to_path(self, tmp_path: pathlib.Path) -> None:
        """
        It can write to a path passed as a ``pathlib.Path``.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        js_path = tmp_path / "shape.js"

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_can_write_to_file(self, tmp_path: pathlib.Path) -> None:
        """
        It can write to a file.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        js_path = tmp_path / "shape.js"

        with open(js_path, "w") as out_file:
            write_js(out_file, value=red_pentagon, varname="redPentagon")

        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_can_write_to_binary_file(self, tmp_path: pathlib.Path) -> None:
        """
        It can write to a file opened in binary mode.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        js_path = tmp_path / "shape.js"

        with open(js_path, "wb") as out_file:
            write_js(out_file, value=red_pentagon, varname="redPentagon")

        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_can_write_to_string_buffer(self) -> None:
        """
        It can write to a string buffer.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        string_buffer = io.StringIO()

        write_js(string_buffer, value=red_pentagon, varname="redPentagon")

        assert (
            string_buffer.getvalue()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_can_write_to_bytes_buffer(self) -> None:
        """
        It can write to a binary buffer.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        bytes_buffer = io.BytesIO()

        write_js(bytes_buffer, value=red_pentagon, varname="redPentagon")

        assert (
            bytes_buffer.getvalue()
            == b'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_fails_if_file_is_read_only(self, tmp_path: pathlib.Path) -> None:
        """
        It cannot write to a file open in read-only mode.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        js_path = tmp_path / "shape.js"
        js_path.write_text("// empty file")

        with pytest.raises(io.UnsupportedOperation):
            with open(js_path, "r") as out_file:
                write_js(out_file, value=red_pentagon, varname="redPentagon")

    def test_throws_typeerror_if_cannot_write(self) -> None:
        """
        Writing to something that can't be written to throws a ``TypeError``.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        with pytest.raises(TypeError):
            write_js(
                ["this", "is", "not", "a", "file"],  # type: ignore
                value=red_pentagon,
                varname="redPentagon",
            )

    def test_fails_if_cannot_write_file(self) -> None:
        """
        Writing to the root folder throws an IsADirectoryError.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        with pytest.raises(IsADirectoryError):
            write_js("/", value=red_pentagon, varname="redPentagon")

    def test_fails_if_target_is_folder(self, tmp_path: pathlib.Path) -> None:
        """
        Writing to a folder throws an IsADirectoryError.
        """
        assert tmp_path.is_dir()

        red_pentagon = {"sides": 5, "colour": "red"}

        with pytest.raises(IsADirectoryError):
            write_js(tmp_path, value=red_pentagon, varname="redPentagon")

    def test_creates_parent_directory(self, tmp_path: pathlib.Path) -> None:
        """
        If the parent directory of the output path doesn't exist, it is
        created before the file is written.
        """
        js_path = tmp_path / "1/2/3/shape.js"
        red_pentagon = {"sides": 5, "colour": "red"}

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        assert js_path.exists()
        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )


class TestAppendToArray:
    """
    Tests for the ``append_to_js_array`` function.
    """

    @pytest.mark.parametrize(
        "text",
        [
            'const fruit = ["apple", "banana", "coconut"];\n',
            'const fruit = ["apple","banana", "coconut"];',
            'const fruit = [\n  "apple",\n  "banana",\n  "coconut"\n];\n',
            'const fruit = [\n  "apple",\n  "banana",\n  "coconut"\n];',
            'const fruit = [\n  "apple",\n  "banana",\n  "coconut"\n]',
        ],
    )
    def test_can_append_array_value(self, js_path: pathlib.Path, text: str) -> None:
        """
        After you append an item to an array, you can retrieve the
        updated array.

        This is true regardless of what the trailing whitespace in the
        original file looks like.
        """
        js_path.write_text(text)

        append_to_js_array(js_path, value="damson")
        assert read_js(js_path, varname="fruit") == [
            "apple",
            "banana",
            "coconut",
            "damson",
        ]

    def test_can_mix_types(self, js_path: pathlib.Path) -> None:
        """
        Arrays can contain a mixture of different types.
        """
        write_js(js_path, value=["apple", "banana", "coconut"], varname="fruit")
        append_to_js_array(js_path, value=["damson"])
        assert read_js(js_path, varname="fruit") == [
            "apple",
            "banana",
            "coconut",
            ["damson"],
        ]

    def test_error_if_file_doesnt_look_like_array(self, js_path: pathlib.Path) -> None:
        """
        Appending to a file which doesn't contain a JSON array throws
        a ValueError.
        """
        red_pentagon = {"sides": 5, "colour": "red"}

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        with pytest.raises(ValueError, match="does not look like an array"):
            append_to_js_array(js_path, value=["yellow"])

    def test_error_if_path_doesnt_exist(self, js_path: pathlib.Path) -> None:
        """
        Appending to the path of a non-existent file throws FileNotFoundError.
        """
        with pytest.raises(FileNotFoundError):
            append_to_js_array(js_path, value="alex")

    def test_error_if_path_is_dir(self, tmp_path: pathlib.Path) -> None:
        """
        Appending to a path which is a directory throws IsADirectoryError.
        """
        with pytest.raises(IsADirectoryError):
            append_to_js_array(tmp_path, value="alex")

    def test_indentation_is_consistent(self, tmp_path: pathlib.Path) -> None:
        """
        If you append to an array, the file looks as if you'd read and rewritten
        the whole thing with ``write_js()``.
        """
        js_path1 = tmp_path / "data1.js"
        js_path2 = tmp_path / "data2.js"

        # We use deliberately large value, so they won't be compressed
        # by the custom encoder.
        value = ["1" * 10, "2" * 20, "3" * 30]
        appended_value = ["4" * 40, "5" * 50, "6" * 60]

        write_js(js_path1, varname="numbers", value=value)
        append_to_js_array(js_path1, value=appended_value)

        write_js(js_path2, varname="numbers", value=value + [appended_value])

        assert js_path1.read_text() == js_path2.read_text()


class TestAppendToObject:
    """
    Tests for the ``append_to_js_object`` function.
    """

    @pytest.mark.parametrize(
        "text",
        [
            'const redPentagon = {"colour": "red", "sides": 5};\n',
            'const redPentagon = {"colour": "red", "sides": 5};',
            'const redPentagon = {\n  "colour": "red",\n  "sides": 5\n};\n',
            'const redPentagon = {\n  "colour": "red",\n  "sides": 5\n};',
            'const redPentagon = {\n  "colour": "red",\n  "sides": 5\n}',
        ],
    )
    def test_append_to_js_object(self, js_path: pathlib.Path, text: str) -> None:
        """
        After you add a key/value pair to an object, you can retrieve the
        updated object.

        This is true regardless of what the trailing whitespace in the
        original file looks like.
        """
        js_path.write_text(text)

        assert read_js(js_path, varname="redPentagon") == {"colour": "red", "sides": 5}

        append_to_js_object(js_path, key="sideLengths", value=[1, 2, 3, 4, 5])
        assert read_js(js_path, varname="redPentagon") == {
            "colour": "red",
            "sides": 5,
            "sideLengths": [1, 2, 3, 4, 5],
        }

    def test_indentation_is_consistent(self, tmp_path: pathlib.Path) -> None:
        """
        If you append to an object, the file looks as if you'd read and
        rewritten the whole thing with ``write_js()``.
        """
        js_path1 = tmp_path / "data1.js"
        js_path2 = tmp_path / "data2.js"

        # We pick a deliberately large value, so it won't be compressed
        # by the custom encoder.
        value = ["1" * 10, "2" * 20, "3" * 30]

        write_js(js_path1, varname="shape", value={"colour": "red"})
        append_to_js_object(js_path1, key="sides", value=value)

        write_js(
            js_path2,
            varname="shape",
            value={"colour": "red", "sides": value},
        )

        assert js_path1.read_text() == js_path2.read_text()

    def test_error_if_file_doesnt_look_like_object(self, js_path: pathlib.Path) -> None:
        """
        Appending to a file which doesn't contain a JSON object throws
        a ValueError.
        """
        shapes = ["apple", "banana", "cherry"]

        write_js(js_path, value=shapes, varname="fruit")

        with pytest.raises(ValueError, match="does not look like an object"):
            append_to_js_object(js_path, key="sideLengths", value=[5, 5, 6, 6, 6])

    def test_error_if_path_doesnt_exist(self, js_path: pathlib.Path) -> None:
        """
        Appending to the path of a non-existent file throws FileNotFoundError.
        """
        with pytest.raises(FileNotFoundError):
            append_to_js_object(js_path, key="name", value="alex")

    def test_error_if_path_is_dir(self, tmp_path: pathlib.Path) -> None:
        """
        Appending to a path which is a directory throws IsADirectoryError.
        """
        with pytest.raises(IsADirectoryError):
            append_to_js_object(tmp_path, key="name", value="alex")


class TestRoundTrip:
    """
    A "round trip" is a test that we can use one function to store a value,
    and another function to retrieve it.

    It checks that the functions are consistent with each other, and aren't
    losing any information along the way.
    """

    @pytest.mark.parametrize(
        "value",
        [
            "hello world",
            5,
            None,
            ["1", "2", "3"],
            {"colour": "red", "sides": 5},
            'a string with "double quotes"',
            "this is const myTestVariable",
            "const myTestVariable = ",
        ],
    )
    def test_can_read_and_write_value(
        self, js_path: pathlib.Path, value: typing.Any
    ) -> None:
        """
        After you write a value with ``write_js()``, you get the same value
        back when you call ``read_js()``.
        """
        write_js(js_path, value=value, varname="myTestVariable")
        assert read_js(js_path, varname="myTestVariable") == value

    def test_can_append_to_file(self, js_path: pathlib.Path) -> None:
        """
        After you append a value to an array, you can read the entire file
        and get the updated array.
        """
        write_js(js_path, value=["apple", "banana", "coconut"], varname="fruit")
        append_to_js_array(js_path, value="damson")
        assert read_js(js_path, varname="fruit") == [
            "apple",
            "banana",
            "coconut",
            "damson",
        ]
