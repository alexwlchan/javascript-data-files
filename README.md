# python-js-files

This is a collection of Python functions for manipulating JavaScript "data files" -- that is, JavaScript files that define a single variable with a JSON value.

This is an example of a JavaScript data file:

```javascript
const shape = { "sides": 5, "colour": "red" };
```

Think of this module as the JSON module, but for JavaScript files.

## API

*   You can read a JavaScript file with `read_js(path, varname)`
*   You can write a JavaScript file with `write_js(path, value, varname)`

## Why not use JSON files?

## License

MIT.
