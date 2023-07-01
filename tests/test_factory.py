from next import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    # assert response.data == b'Library "3 Books"'
    # assert 'Library "3 Books"' in str(response.data)
