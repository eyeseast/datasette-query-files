# datasette-query-files

[![PyPI](https://img.shields.io/pypi/v/datasette-query-files.svg)](https://pypi.org/project/datasette-query-files/)
[![Changelog](https://img.shields.io/github/v/release/eyeseast/datasette-query-files?include_prereleases&label=changelog)](https://github.com/eyeseast/datasette-query-files/releases)
[![Tests](https://github.com/eyeseast/datasette-query-files/workflows/Test/badge.svg)](https://github.com/eyeseast/datasette-query-files/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/eyeseast/datasette-query-files/blob/main/LICENSE)

Write Datasette canned queries as plain SQL files.

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-query-files

Or using `pip` or `pipenv`:

    pip install datasette-query-files
    pipenv install datasette-query-files

## Usage

This plugin will look for [canned queries](https://docs.datasette.io/en/stable/sql_queries.html#canned-queries) in the filesystem, in addition any defined in metadata.

Let's say you're working in a directory called `project-directory`, with a database file called `my-project.db`. Start by creating a `queries` directory with a `my-project` directory inside it. Any SQL file inside that `my-project` folder will become a canned query that can be run on the `my-project` database. If you have a `query-name.sql` file and a `query-name.json` (or `query-name.yml`) file in the same directory, the JSON file will be used as query metadata.

```
project-directory/
  my-project.db
  queries/
    my-project/
      query-name.sql # a query
      query-name.yml # query metadata
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-query-files
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
