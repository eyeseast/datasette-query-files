from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-query-files",
    description="Write Datasette canned queries as plain SQL files",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Chris Amico",
    url="https://github.com/eyeseast/datasette-query-files",
    project_urls={
        "Issues": "https://github.com/eyeseast/datasette-query-files/issues",
        "CI": "https://github.com/eyeseast/datasette-query-files/actions",
        "Changelog": "https://github.com/eyeseast/datasette-query-files/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_query_files"],
    entry_points={"datasette": ["query_files = datasette_query_files"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    python_requires=">=3.7",
)
