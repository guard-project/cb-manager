from falcon import testing

import pytest

@pytest.fixture()
def client():
    return testing.TestClient(myapp.create())


def test_get_message(client):
    doc = {u'message': u'Hello world!'}

    result = client.simulate_get('/messages/42')
    assert result.json == doc
