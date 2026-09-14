def test_register_user(client):
    response = client.post('/users/register', json={
        'email': 'test@example.com',
        'password': 'secretpassword123'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'test@example.com'
    assert 'password' not in data
    assert 'hashed_password' not in data


def test_register_duplicate_email(client):
    client.post('/users/register', json={
        'email': 'duplicate@example.com',
        'password': 'secretpassword123'
    })

    response = client.post('users/register', json={
        'email': 'duplicate@example.com',
        'password': 'differentpassword123'
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post('/users/register', json={
        'email': 'logintest@example.com',
        'password': 'secretpassword123'
    })

    response = client.post('/users/login', data={
        'username': 'logintest@example.com',
        'password': 'secretpassword123'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_login_wrong_password(client):
    client.post("/users/register", json={
        "email": "logintest2@example.com",
        "password": "secretpassword123",
    })
    response = client.post("/users/login", data={
        "username": "logintest2@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401