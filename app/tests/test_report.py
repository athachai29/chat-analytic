from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_reports():
    response = client.get("/api/fa778f8cfa1e4a3f6331299df0c2c4520c150fce")

    assert response.status_code == 200
    assert response.json() == {
        "report_code": "fa778f8cfa1e4a3f6331299df0c2c4520c150fce",
        "report": {
            "basic_stats": {
                "total_messags": 213,
                "total_medias": 28,
                "total_calleds": 3,
            },
            "basic_stats_of_each_author": [
                {
                    "author": "ภ",
                    "total_messages": 108,
                    "total_medias": 17,
                    "total_calleds": 3,
                },
                {
                    "author": "P",
                    "total_messages": 105,
                    "total_medias": 11,
                    "total_calleds": 0,
                },
            ],
        },
    }
