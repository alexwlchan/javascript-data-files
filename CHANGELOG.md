# CHANGELOG

## v1.4.1 - 2025-08-15

Fix the yanked v1.4.0 release, and make sure it includes the correct code.

## v1.4.0 - 2025-08-15

Add an `ensure_ascii` parameter to `write_js`.
If `True`, all incoming ASCII characters will be escaped, otherwise they will be left as-is.
Default is `False`.

This changes the default output of `write_js`.
Before, it would escape any incoming ASCII characters, for example `“hello world”` would be encoded as:

```json
"\u201chello world\u201d"
```

With the new behaviour, it will be encoded as:

```json
“hello world”
```

unless you explicitly pass `ensure_ascii=True`.

This mirrors the parameter on the builtin `json.dumps()`, but with a different default.

## v1.3.0 - 2025-05-05

Add a `sort_keys` parameter to `write_js`.
If `True`, dictionaries with be serialised to JSON sorted by key.
Default `False`.

This mirrors the parameter on the builtin `json.dumps()`.

## v1.2.3 - 2025-05-04

Tweak the error message introduced in v1.2.2 -- JSON objects are **name**/value pairs, not key/value pairs.

## v1.2.2 - 2025-05-03

Duplicate keys in JSON objects are now rejected as an error.

For example, consider the following JavaScript:

```javascript
const shape = {"sides": "5", "colour": "red", "sides": 4};
```

These duplicate keys are technically allowed by the JSON specification, but are always a mistake when I encounter them.
Many JSON parsers will silently drop the first instance of `sides`, including both Python's and web browsers.

Previously `read_js` would read this file and silently drop the first key, but now it throws a `ValueError` and prompts you to de-duplicate the key.

## v1.2.1 - 2025-04-13

Fix a bug in the validation of `typing.Union[A, B]` where both types are a `TypedDict`.

The validation is stricter, and will require an exact match to either `A` or `B` -- previously it was possible for data to validate that was only a "partial" match, and this could cause data to be lost.
This was only possible in cases where the fields of `A` were a strict subset of the fields of `B`, and you passed a value which used more fields than `A` but less than `B`.

For example, consider the following type:

```python
BasicShape = typing.TypedDict("Shape", {"sides": int, })
NamedShape = typing.TypedDict("Shape", {"sides": int, "colour": str, "name": str })

Shape = BasicShape | NamedShape
```

if you passed the data:

```javascript
const shape = {"sides": "5", "colour": "red"};
```

this isn't a strict match for `BasicShape` or `NamedShape`, but would be incorrectly validated and returned as `{'sides': 5}`.

Now this throws a `pydantic.ValidationError`.

## v1.2.0 - 2025-03-07

This adds a new function `read_typed_js`, which is like `read_js` but will additionally validate the data against a type you specify.

*   `read_js()` returns `typing.Any`, and will always return something if the file contains valid JSON
*   `read_typed_js` returns `T`, where `T` is the type you specify as `model`.
    This will only return if the file contains JSON that matches the type, and otherwise it will throw a `pydantic.ValidationError`.

This is useful if you want to check your data or you write typed Python.

You need to install the typed extra to get this function, i.e. `pip install javascript-data-files[typed]`.

## v1.1.1 - 2025-01-10

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
