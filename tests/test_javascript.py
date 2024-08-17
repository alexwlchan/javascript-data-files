import pathlib
import typing

import pytest

from javascript import append_to_js_array, read_js, write_js


class TestReadJs:
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
    def test_can_read_file(self, tmp_path: pathlib.Path, text: str) -> None:
        js_path = tmp_path / "shape.js"
        js_path.write_text(text)

        assert read_js(js_path, varname="redPentagon") == {"sides": 5, "colour": "red"}

    def test_non_existent_file_is_error(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_js("doesnotexist.js", varname="shape")

    def test_non_json_value_is_error(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "total.js"
        js_path.write_text("const sum = 1 + 1 + 1;")

        with pytest.raises(ValueError):
            read_js(js_path, varname="sum")

    def test_incorrect_varname_is_error(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "shape.js"
        js_path.write_text(
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

        with pytest.raises(
            ValueError, match="does not start with JavaScript `const` declaration"
        ):
            read_js(js_path, varname="blueTriangle")


class TestWriteJs:
    def test_can_write_file(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "shape.js"
        red_pentagon = {"sides": 5, "colour": "red"}

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

    def test_fails_if_cannot_write_file(self) -> None:
        red_pentagon = {"sides": 5, "colour": "red"}

        with pytest.raises(OSError):
            write_js("/", value=red_pentagon, varname="redPentagon")

    def test_creates_parent_directory(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "1/2/3/shape.js"
        red_pentagon = {"sides": 5, "colour": "red"}

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        assert js_path.exists()
        assert (
            js_path.read_text()
            == 'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )


class TestAppendToArray:
    def test_can_mix_types(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "food.js"

        write_js(js_path, value=["apple", "banana", "coconut"], varname="fruit")
        append_to_js_array(js_path, value=["damson"])
        assert read_js(js_path, varname="fruit") == [
            "apple",
            "banana",
            "coconut",
            ["damson"],
        ]

    def test_error_if_file_doesnt_look_like_array(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "shape.js"
        red_pentagon = {"sides": 5, "colour": "red"}

        write_js(js_path, value=red_pentagon, varname="redPentagon")

        with pytest.raises(ValueError, match="does not look like an array"):
            append_to_js_array(js_path, value=["yellow"])


class TestRoundTrip:
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
        self, tmp_path: pathlib.Path, value: typing.Any
    ) -> None:
        js_path = tmp_path / "testdata.js"

        write_js(js_path, value=value, varname="myTestVariable")
        assert read_js(js_path, varname="myTestVariable") == value

    def test_can_append_to_file(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "food.js"

        write_js(js_path, value=["apple", "banana", "coconut"], varname="fruit")
        append_to_js_array(js_path, value="damson")
        assert read_js(js_path, varname="fruit") == [
            "apple",
            "banana",
            "coconut",
            "damson",
        ]