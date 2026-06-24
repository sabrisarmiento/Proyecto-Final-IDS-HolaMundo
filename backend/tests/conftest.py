import os
import sys

os.environ["SECRET_KEY"] = "test-secret"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jwt
import pytest
import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


@pytest.fixture
def make_token():
    def build(nivel, id_usuario=1, id_rol=1):
        return jwt.encode(
            {"id_usuario": id_usuario, "nivel": nivel, "id_rol": id_rol},
            os.environ["SECRET_KEY"],
            algorithm="HS256",
        )

    return build
