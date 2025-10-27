"""
Pytest fixtures for API testing
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.database import Base
from app.models.tables import User, Order, OrderItem
from app.main import app, bcrypt_context
from app.models.dependencies import get_session

# Use in-memory SQLite for tests with shared cache
TEST_DATABASE_URL = "sqlite:///file:testdb?mode=memory&cache=shared&uri=true"


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False, "uri": True},
        poolclass=None,  # Disable pooling for in-memory database
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a fresh database session for each test"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_engine):
    """FastAPI test client with overridden database"""

    # Create a session factory for the test engine
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )

    def override_get_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(test_db):
    """Create a sample regular user"""
    hashed_password = bcrypt_context.hash("testpassword123")
    user = User(
        email="user@example.com",
        username="testuser",
        password=hashed_password,
        active=True,
        admin=False,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_admin(test_db):
    """Create a sample admin user"""
    hashed_password = bcrypt_context.hash("adminpass123")
    admin = User(
        email="admin@example.com",
        username="adminuser",
        password=hashed_password,
        active=True,
        admin=True,
    )
    test_db.add(admin)
    test_db.commit()
    test_db.refresh(admin)
    return admin


@pytest.fixture
def user_token(client, sample_user):
    """Get authentication token for regular user"""
    response = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client, sample_admin):
    """Get authentication token for admin user"""
    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpass123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def sample_order(test_db, sample_user):
    """Create a sample order"""
    order = Order(user_id=sample_user.id, status="PENDING", price=0.0)
    test_db.add(order)
    test_db.commit()
    test_db.refresh(order)
    return order


@pytest.fixture
def sample_order_with_items(test_db, sample_user):
    """Create a sample order with items"""
    order = Order(user_id=sample_user.id, status="PENDING", price=0.0)
    test_db.add(order)
    test_db.commit()
    test_db.refresh(order)

    # Add items
    item1 = OrderItem(
        quantity=2,
        flavor="Pepperoni",
        size="Large",
        unit_price=15.99,
        order_id=order.id,
    )
    item2 = OrderItem(
        quantity=1,
        flavor="Margherita",
        size="Medium",
        unit_price=12.99,
        order_id=order.id,
    )
    test_db.add(item1)
    test_db.add(item2)
    test_db.commit()

    # Calculate total price
    order.price = (item1.quantity * item1.unit_price) + (
        item2.quantity * item2.unit_price
    )
    test_db.commit()
    test_db.refresh(order)

    return order
