A full-featured e-commerce backend built with FastAPI, PostgreSQL and SQLAlchemy, built as a portfolio project to demonstrate practical API design, authentication, relational data modelling and testing.

This project was built and debugged from scratch, working through issues like Alembic migration recovery, SQLAlechemy session lifecyle bugs and a bcrypt version incompatibility.

# Features:
- Authentication and Authorisation
    - User registration with bcrypt hashed passwords
    - OAuth2 login issuing a signed JWT
    - Role based access with admin status required for controlled pathways

- Product Database
    - Full CRUD on Products and Categories
    - One to many relationship between Products and Categories
    - Filtering and sorting options available for both Products and Categories

- Cart and Checkout
    - Cart linked to each authenticated user so there is only one cart per user
    - Add and remove items from stock automatically
    - Checkout validates stock, decreases inventory, records price at time of transaction before clearing the cart in a single transaction

- Order History
    - Users can view their own past orders

- Testing
    - Automated tests with pytest on an isolated test database
    - current testing for authentication, checkout success/failure and ownership

# Project Structure:
app/
├── core/           # config, database connection, security (hashing, JWT)
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic request/response schemas
├── routers/        # API route handlers
├── services/       # business logic (e.g. checkout)
└── main.py         # app entrypoint
alembic/            # database migrations
tests/              # pytest 

# Getting Started:

**Prerequisites**
- Python 3.11+
- PostgreSQL running locally

**Setup**
1. Clone the repo and create a virtual environment:
```bash
git clone <your-repo-url>
cd e-commerce_rest_api
python -m venv venv
source venv/bin/activate
```

2. Install dependancies: `pip install -r requirements.txt`
    - Note bcyrpt is pinned to 4.0.1 due to a compatibility issue with newer bcrypt versions and passlib

3. Create the database: `createdb ecommerce_db`

4. Copy .env.example to .env and fill in your values: `cp .env.example .env`

    DATABASE_URL=postgresql://<your_user>@localhost:5432/ecommerce_db
    SECRET_KEY=<a-random-secret-string>

5. Run migrations: `alembic upgrade head`

6. Start the server: `uvicorn app.main:app --reload

7. Open the interactive API docs at http://127.0.0.1:8000/docs

# API Overview

| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| POST   | `/users/register` | Register a new account | — |
| POST   | `/users/login` | Log in, receive a JWT | — |
| GET    | `/products/` | List/filter/sort products | — |
| POST   | `/products/` | Create a product | Admin |
| PATCH  | `/products/{id}` | Update a product | Admin |
| DELETE | `/products/{id}` | Delete a product | Admin |
| GET    | `/categories/` | List categories | — |
| POST   | `/categories/` | Create a category | Admin |
| PATCH  | `/categories/{id}` | Update a category | Admin |
| DELETE | `/categories/{id}` | Delete a category | Admin |
| GET    | `/cart/` | View your cart | User |
| POST   | `/cart/items` | Add an item to your cart | User |
| DELETE | `/cart/items/{id}` | Remove an item from your cart | User |
| POST   | `/cart/checkout` | Convert your cart into an order | User |
| GET    | `/orders/` | View your order history | User |
| GET    | `/orders/{id}` | View a single order | User |

Full documentation, including request/response schemas is available at the `/docs` once the server is running.

# Design Notes

Some deliberate design decisions worth noting:
- Historical pricing: `OrderItem` stores `price_at_purchase` separately from `Product.price` so order history remains accurate even if the product price changes at a later date.
- Atomic Checkout: stock validation happens for the entire cart before any changes are committed so if a single item fails validation there aren't any partial changes to the database.
- Ownership: every user-scoped query filters by the authenticated user's ID at the database level so user's can't access another's data
- Service layer: checkout logic lives in `/services` outside of the HTTP layer which makes it testable without running a request

# What I'd Add Next:
- Docker and cloud deployment
- Refresh tokens
- Admin endpoints for order managment

