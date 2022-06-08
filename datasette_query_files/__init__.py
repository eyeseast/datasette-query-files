import aiofiles
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
        if not db_dir.is_dir():
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

    return {"sql": sql}
