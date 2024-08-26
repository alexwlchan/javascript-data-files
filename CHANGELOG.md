# CHANGELOG

## v1.0.1 - 2024-08-26

When you call `append_to_js_array()` or `append_to_js_object()`, previously the new value would all be smushed onto one line.
Now it's written with 2 spaces of indentation, to match `write_js()`.

## v1.0.0 - 2024-08-24

Initial release.  This includes four functions:

*   Read a JavaScript file with `read_js(path, varname)`
*   Write a JavaScript file with `write_js(path, value, varname)`
*   Append an item to a JavaScript array with `append_to_js_array(path, value)`
*   Append a key-value pair to a JavaScript object with `append_to_js_object(path, key, value)`

## v0.0.1 - 2024-08-24

Initial release on PyPI, to test the release mechanism.
