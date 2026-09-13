def test_create_and_list_products(client):
    response = client.get('/products/')
    assert response.status_code == 200
    assert response.json() == []


