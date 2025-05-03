# CONTRIBUTING

You can set up a local development environment by cloning the repo and installing dependencies:

```shell
git clone https://github.com/alexwlchan/javascript-data-files.git
cd javascript-data-files
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you want to run tests, install the dev dependencies and run the tests:

```shell
# Activate the virtualenv and install dev dependencies
source .venv/bin/activate
pip install -r dev_requirements.txt

# Check formatting
ruff check .
ruff format --check .

# Check docstrings
interrogate -vv

# Check types
mypy src tests

# Run tests
coverage run -m pytest tests
coverage report
```

To make changes:

1.  Create a new branch
2.  Push your changes to GitHub
3.  Open a pull request
4.  Fix any issues flagged by GitHub Actions (including tests, code linting, and type checking)
6.  Merge it!

To create a new version on PyPI:

1.  Update the version in `src/javascript_data_files/__init__.py`
2.  Add release notes in `CHANGELOG.md` and push a new tag to GitHub
3.  Deploy the release using twine:

    ```console
    $ python3 -m build
    $ python3 -m twine upload dist/* --username=__token__
    ```

    You will need [a PyPI API token](https://pypi.org/help/#apitoken) to publish packages.


