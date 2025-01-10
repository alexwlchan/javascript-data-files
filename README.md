# javascript-data-files

This is a collection of Python functions for manipulating JavaScript "data files" -- that is, JavaScript files that define a single variable with a JSON value.

This is an example of a JavaScript data file:

```javascript
const shape = { "sides": 5, "colour": "red" };
```

Think of this module as the JSON module, but for JavaScript files.

These data files are meant to be both human- and machine-readable.

## Usage

*   You can read a JavaScript file with `read_js(path, varname)`
*   You can write a JavaScript file with `write_js(path, value, varname)`
*   You can append an item to a JavaScript array with `append_to_js_array(path, value)`
*   You can append a key-value pair to a JavaScript object with `append_to_js_object(path, key, value)`

## Installation

You have two options:

1.  Copy the file `src/javascript` folder into your project.
    You probably want to copy the tests as well.

2.  Install the package using pip:

    ```console
    $ pip install javascript-data-files
    ```

## Why not use JSON files?

If you've opening an HTML file from disk, you can load data from a local JavaScript file, for example:

```html
<script src="file://users/alexwlchan/repos/javascript-data-files/data.js"></script>
```

This is the only way to load data from an external file from an HTML file you've opened locally -- you can't do this with a JSON file, for example.

I have a lot of HTML files and local sites I build with an HTML viewer and metadata in a JavaScript file.
The convenience of this approach outweighs the mild annoyance of having to store data in JavaScript, not JSON.

## License

MIT.
