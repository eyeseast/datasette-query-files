import pathlib
import pytest
import sqlite3
import httpx
from datasette.app import Datasette
from datasette.app import DatasetteClient

PLUGIN_NAME = "datasette-query-files"
TESTS = pathlib.Path(__file__).parent
LEGISLATORS = TESTS / "legislators.db"
QUERIES = TESTS / "queries"

SQL_FILES = {
    "presidents": QUERIES / "legislators" / "presidents.sql",
    "women_senators": QUERIES / "legislators" / "women_senators.sql",
}

METADATA = {
    "presidents": {"title": "All the presidents"},
    "women_senators": {"title": "Women in the Senate"},
}

CREATE_WRITE_TABLE = """
create table messages (user_id text, message text, datetime text);
"""


@pytest.fixture
def ds(tmp_path):
    WRITABLE = tmp_path / "writable.db"

    writable = sqlite3.connect(WRITABLE)
    writable.executescript(CREATE_WRITE_TABLE)

    yield Datasette(
        [LEGISLATORS, WRITABLE],
        metadata={"plugins": {PLUGIN_NAME: {"query_directory": QUERIES}}},
    )

    WRITABLE.unlink()


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


@pytest.mark.asyncio
async def test_write_message(ds):
    assert ds._root_token is not None
    token = ds._root_token
    async with httpx.AsyncClient(
        app=ds.app(),
        base_url="http://localhost",
        cookies={"ds_actor": ds.sign({"a": {"id": "root"}}, "actor")},
    ) as client:

        url = ds.urls.query("writable", "write_message")
        r1 = await client.get(url)
        assert 200 == r1.status_code

        csrftoken = r1.cookies["ds_csrftoken"]
        r2 = await client.post(
            url,
            data={
                "message": "Hello, world!",
                "csrftoken": csrftoken,
            },
            headers={"Accept": "application/json"},
        )

        assert 200 == r2.status_code

        data = r2.json()

        assert data["ok"]


@pytest.mark.asyncio
async def _test_write_message(ds):
    cookie = ds.sign({"a": {"id": "test"}}, "actor")
    url = ds.urls.query("writable", "write_message")

    resp = await ds.client.post(
        url,
        data={"message": "Hello, world!"},
        headers={"Accept": "application/json"},
        cookies={"ds_actor": cookie},
    )

    assert 200 == resp.status_code
