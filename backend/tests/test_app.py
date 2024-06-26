from flask.testing import FlaskClient


def test_index(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.data == b"Hello from Flask!"


def test_upload(client: FlaskClient) -> None:
    data = {"image": (open("../sample.png", "rb"), "sample.png")}
    response = client.post("/upload", data=data)
    assert response.data == b"5132bfb3723cbc370fa301c7579195ea"
