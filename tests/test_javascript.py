import pathlib

import pytest

from javascript import read_js


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
