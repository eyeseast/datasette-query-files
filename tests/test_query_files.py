import pathlib
import pytest
from datasette.app import Datasette

PLUGIN_NAME = "datasette-query-files"
TESTS = pathlib.Path(__file__).parent
DATABASE = TESTS / "legislators.db"
QUERIES = TESTS / "queries"

SQL_FILES = {
    "presidents": QUERIES / "legislators" / "presidents.sql",
    "women_senators": QUERIES / "legislators" / "women_senators.sql",
}

METADATA = {
    "presidents": {"title": "All the presidents"},
    "women_senators": {"title": "Women in the Senate"},
}


@pytest.fixture
def ds():
    return Datasette(
        [DATABASE], metadata={"plugins": {PLUGIN_NAME: {"query_directory": QUERIES}}}
    )


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert PLUGIN_NAME in installed_plugins


@pytest.mark.asyncio
async def test_query_exists(ds):
    presidents_query = SQL_FILES["presidents"]
    assert presidents_query.exists()  # make sure it's not broken

    url = ds.urls.database("legislators", format="json")
    resp = await ds.client.get(url)
    data = resp.json()
    queries = data["queries"]  # let this error if it errors

    assert len(queries) > 0
    assert presidents_query.stem in [q["name"] for q in queries]


@pytest.mark.asyncio
async def test_query_results(ds):
    url = ds.urls.query("legislators", "presidents", format="json")
    resp = await ds.client.get(url)

    assert resp.status_code == 200

    data = resp.json()

    # 45 presidents, counting Grover Cleveland once
    assert len(data["rows"]) == 45


@pytest.mark.asyncio
async def test_query_metadata(ds):
    url = ds.urls.database("legislators", format="json")

    resp = await ds.client.get(url)
    data = resp.json()
    queries = {q["name"]: q for q in data["queries"]}

    for name, path in SQL_FILES.items():
        metadata = METADATA[name]
        query = queries[name]

        assert metadata["title"] == query["title"]
