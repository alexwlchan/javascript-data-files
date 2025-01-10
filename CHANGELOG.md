# CHANGELOG

## v1.1.1

Tweak the way the JavaScript is encoded to make it slightly more compact and readable -- in particular, short lists will now be encoded as a single line, rather than split across multiple lines.

Before:

```json
[
  1,
  2,
  3
]
```

After:

```json
[1, 2, 3]
```

The value is the same but should be more readable.
This opens the door to more readability improvements in the future.

## v1.1.0 - 2025-01-10

You can now call `write_js()` with a file-like object.
This can be text I/O or as binary I/O.

This gives you more control over how the file is written -- for example, you can open the file in "exclusive creation" mode to prevent overwriting an existing file:

```python
with open("shape.js", "x") as out_file:
    write_js(
        out_file,
        value={"sides": 5, "colour": "red"},
        varname="redPentagon"
    )
```

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
