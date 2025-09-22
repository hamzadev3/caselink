from fastapi.testclient import TestClient
from api import app
from db import init_db, DBsession, File
from scan import scan_folder

def setup_module(_):
    init_db()
    # seed DB if empty
    s = DBsession()
    try:
        if not s.query(File).first():
            scan_folder("_sample")
    finally:
        s.close()

def test_search_endpoint_ok():
    client = TestClient(app)
    r = client.get("/search", params={"case": "60012"})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert isinstance(data["results"], list)
