import os

import pytest
from falcon import testing

path = os.path.abspath(__file__)
dir_path = os.path.dirname(os.path.dirname(path))
os.chdir(dir_path)

from api import api  # noqa: E402
from lib.token import create_token  # noqa: E402


@pytest.fixture()
def client():
    return testing.TestClient(api())


def test_exec_env_get(client):
    result = client.simulate_get(
        "/exec-env", headers={"Authorization": create_token()}
    )
    assert result.status_code == 200
