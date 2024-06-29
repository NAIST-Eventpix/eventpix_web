from flask.testing import FlaskClient


def test_index(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200


def test_sample_result_view(client: FlaskClient) -> None:
    response = client.get("/sample_result_view")
    assert response.status_code == 200
