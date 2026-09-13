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