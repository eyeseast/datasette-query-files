# datasette-query-files

[![PyPI](https://img.shields.io/pypi/v/datasette-query-files.svg)](https://pypi.org/project/datasette-query-files/)
[![Changelog](https://img.shields.io/github/v/release/eyeseast/datasette-query-files?include_prereleases&label=changelog)](https://github.com/eyeseast/datasette-query-files/releases)
[![Tests](https://github.com/eyeseast/datasette-query-files/workflows/Test/badge.svg)](https://github.com/eyeseast/datasette-query-files/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/eyeseast/datasette-query-files/blob/main/LICENSE)

Write Datasette canned queries as plain SQL files

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-query-files

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-query-files
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
