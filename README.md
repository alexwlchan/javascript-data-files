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
*   You can append an item to a JavaScript array with `append_to_js_array(path, value)`
*   You can append a key-value pair to a JavaScript object with `append_to_js_object(path, key, value)`

## Installation

Copy the file `src/javascript` folder into your project.
You probably want to copy the tests as well.

Eventually this will be a pip installable package, once I've done some more testing (see [issue #3](https://github.com/alexwlchan/python-js-files/issues/3)).

## Why not use JSON files?

## License

MIT.
