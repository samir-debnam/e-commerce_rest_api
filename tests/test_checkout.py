from app.models.product import Product


def register_and_login(client, email="checkoutuser@example.com", password="secretpassword123"):
    client.post("/users/register", json={"email": email, "password": password})
    response = client.post("/users/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_checkout_success(client, db_session):
    headers = register_and_login(client)
    product = Product(name="Test Widget", price=10.0, stock=5)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    client.post("/cart/items", json={"product_id": product.id, "quantity": 2}, headers=headers)

    response = client.post("/cart/checkout", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 20.0
    assert len(data["items"]) == 1

    db_session.refresh(product)
    assert product.stock == 3 #type: ignore[call-arg]


def test_checkout_insufficient_stock(client, db_session):
    headers = register_and_login(client)

    product = Product(name="Rare Item", price=50.0, stock=1)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    client.post("/cart/items", json={"product_id": product.id, "quantity": 5}, headers=headers)

    response = client.post("/cart/checkout", headers=headers)
    assert response.status_code == 400


def test_checkout_empty_cart(client):
    headers = register_and_login(client, email="emptycart@example.com")

    response = client.post("/cart/checkout", headers=headers)
    assert response.status_code == 400



def test_order_history_scoped_to_user(client, db_session):

    headers_a = register_and_login(client, email="usera@example.com")
    product = Product(name="Widget", price=5.0, stock=10)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    client.post("/cart/items", json={"product_id": product.id, "quantity": 1}, headers=headers_a)
    client.post("/cart/checkout", headers=headers_a)

    headers_b = register_and_login(client, email="userb@example.com")
    response = client.get("/orders/", headers=headers_b)
    assert response.status_code == 200
    assert response.json() == []