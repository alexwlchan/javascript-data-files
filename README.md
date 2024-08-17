# python-js-files

This is a collection of Python functions for manipulating JavaScript "data files" -- that is, JavaScript files that define a single variable with a JSON value.

This is an example of a JavaScript data file:

```javascript
const shape = { "sides": 5, "colour": "red" };
```

Think of this module as the JSON module, but for JavaScript files.

## Usage

*   You can read a JavaScript file with `read_js(path, varname)`
*   You can write a JavaScript file with `write_js(path, value, varname)`
*   You can append an item to a JavaScript array with `append_js_array_value(path, value)`

## Installation

## Why not use JSON files?

## License

MIT.
