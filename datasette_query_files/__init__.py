import json
import yaml
import aiofiles
import aiofiles.os
from pathlib import Path
from datasette import hookimpl

PLUGIN_NAME = "datasette-query-files"


@hookimpl
def canned_queries(datasette, database):
    config = datasette.plugin_config(PLUGIN_NAME) or {}
    query_directory = Path(config.get("query_directory", "queries")).resolve()
    db_dir = query_directory / database

    async def inner():
        queries = {}
        if not await aiofiles.os.path.isdir(db_dir):
            return queries

        for path in db_dir.iterdir():
            if path.suffix == ".sql":
                queries[path.stem] = await get_canned_query(path, database)

        return queries

    return inner


async def get_canned_query(path, database):
    async with aiofiles.open(path) as f:
        sql = await f.read()

    # todo look for metadata
    metadata_paths = [
        path.parent / (path.stem + ext) for ext in [".json", ".yml", ".yaml"]
    ]
    metadata = await get_metadata(*metadata_paths)
    metadata["sql"] = sql
    return metadata


async def get_metadata(*paths):
    metadata = {}
    content = format = None

    for path in paths:
        if await aiofiles.os.path.isfile(path):
            async with aiofiles.open(path) as f:
                content = await f.read()
                format = path.suffix
                break

    if content:
        metadata = parse(content, format)

    return metadata


def parse(content, format):
    if format == ".json":
        return json.loads(content)

    if format in {".yaml", ".yml"}:
        return yaml.load(content, Loader=yaml.SafeLoader)

    return {}