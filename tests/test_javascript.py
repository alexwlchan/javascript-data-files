import pathlib

import pytest

from javascript import read_js, write_js


class TestReadJs:
    def test_can_read_file(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "shape.js"
        js_path.write_text(
            'const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n};\n'
        )

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

    def test_no_trailing_semicolon_is_error(self, tmp_path: pathlib.Path) -> None:
        js_path = tmp_path / "shape.js"
        js_path.write_text('const redPentagon = {\n  "sides": 5,\n  "colour": "red"\n}')

        with pytest.raises(ValueError, match="does not end with a trailing semicolon"):
            read_js(js_path, varname="redPentagon")


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
