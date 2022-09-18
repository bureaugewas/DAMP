import json


def test_get_metadata(client):
    response = client.get('/metadata')

    assert response.status_code == 200
    assert json.loads(response.data)['test name'] == "/api/fetch/test_name"


def test_get_data(client):
    response = client.get("/api/fetch/test_name")

    assert response.status_code == 200
    assert b'test' in response.data


def test_create_endpoint(client):
    client_id = 'test'
    client_secret = 'test'
    name = "test name 3"
    endpoint = "/api/fetch/test_name_3"
    data = {"test": 1, "test2": 2}

    headers = {'Content-type': 'application/json'}
    body = {"name": name,
            "json_validation": 1,
            "status": "Active",
            "availability": "Public",
            "daily_rate_limit": 200,
            "data": data}

    response = client.post('/api/upload',
                           headers=headers,
                           json=body,
                           auth=(client_id, client_secret))

    assert response.status_code == 200
    assert b'Successfully created endpoint: /api/fetch/test_name_3' in response.data

    response = client.get('/metadata')

    assert response.status_code == 200
    assert json.loads(response.data)[name] == endpoint

    response = client.get(endpoint)

    assert response.status_code == 200
    assert str(data) in str(json.loads(response.data))


def test_update_endpoint(client):
    client_id = 'test'
    client_secret = 'test'
    name = 'test name'
    endpoint = "/api/fetch/test_name"

    headers = {'Content-type': 'application/json'}
    body = {"name": name,
            "availability": "Private",
            "json_validation": 0,
            "data": "changed data"}

    response = client.put('/api/update',
                          headers=headers,
                          json=body,
                          auth=(client_id, client_secret))

    assert response.status_code == 200
    assert b'Successfully updated endpoint: /api/fetch/test_name' in response.data

    # Test getting private data using client id and secret
    response = client.get(endpoint)
    assert response.status_code == 404

    # Test getting private data using client id and secret
    response = client.post(endpoint,
                           headers=headers,
                           auth=(client_id, client_secret))

    assert response.status_code == 200
    assert b'changed data' in response.data


def test_delete_endpoint(client):
    client_id = 'test'
    client_secret = 'test'
    endpoint = "/api/fetch/test_name"
    body = {"name": "test name"}

    headers = {'Content-type': 'application/json'}
    response = client.delete('/api/delete',
                             headers=headers,
                             json=body,
                             auth=(client_id, client_secret))

    assert response.status_code == 200
    assert b'Successfully deleted endpoint: /api/fetch/test_name' in response.data

    # Test data not being available anymore
    response = client.get(endpoint)
    assert response.status_code == 404
