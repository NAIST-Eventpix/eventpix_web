from typing import Generator

import pytest
from eventpix.app import app
from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def client() -> Generator[FlaskClient, None, None]:
    flask_app = app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()
