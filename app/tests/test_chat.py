from fastapi.testclient import TestClient
import os

from ..main import app

client = TestClient(app)


def test_create_upload_chats():
    filename = os.path.join(
        os.path.dirname(__file__), "../../static/sample_line_chat.txt"
    )
    with open(filename) as f:
        data = f.read()

    response = client.post("/api/", files={"file": data})

    assert response.status_code == 200
    assert response.json() == {"chat_id": "fa778f8cfa1e4a3f6331299df0c2c4520c150fce"}
