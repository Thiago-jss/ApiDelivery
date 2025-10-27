"""
Order management endpoint tests
"""
import pytest


@pytest.mark.orders
class TestOrderEndpoints:
    """Test order management endpoints"""

    def test_orders_home_requires_auth(self, client):
        """Test that orders endpoint requires authentication"""
        response = client.get("/orders/")
        assert response.status_code == 401

    def test_orders_home_with_auth(self, client, user_token):
        """Test orders home endpoint with authentication"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/orders/", headers=headers)
        
        assert response.status_code == 200
        assert "message" in response.json()

    def test_create_order_success(self, client, user_token, sample_user, test_db):
        """Test successful order creation"""
        headers = {"Authorization": f"Bearer {user_token}"}
        payload = {"user_id": sample_user.id}
        
        response = client.post("/orders/order", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Order successfully created" in data["message"]

    def test_create_order_without_auth(self, client, sample_user):
        """Test order creation without authentication"""
        payload = {"user_id": sample_user.id}
        response = client.post("/orders/order", json=payload)
        
        assert response.status_code == 401

    def test_list_all_orders_admin_only(self, client, user_token, admin_token):
        """Test that only admins can list all orders"""
        # Regular user should get 403
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/orders/list", headers=headers)
        assert response.status_code == 403
        
        # Admin should succeed
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/orders/list", headers=admin_headers)
        assert response.status_code == 200
        assert "orders" in response.json()

    def test_list_user_orders(self, client, user_token, sample_order):
        """Test listing user's own orders"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/orders/list/order-user", headers=headers)
        
        assert response.status_code == 200
        orders = response.json()
        assert isinstance(orders, list)
        assert len(orders) >= 1

    def test_add_item_to_order(self, client, user_token, sample_order, test_db):
        """Test adding item to order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        payload = {
            "quantity": 2,
            "flavor": "Pepperoni",
            "size": "Large",
            "unit_price": 15.99
        }
        
        response = client.post(
            f"/orders/order/add-item/{sample_order.id}",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Item successfully created" in data["message"]
        assert "item_id" in data
        assert "order_price" in data

    def test_add_item_to_nonexistent_order(self, client, user_token):
        """Test adding item to non-existent order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        payload = {
            "quantity": 1,
            "flavor": "Test",
            "size": "Medium",
            "unit_price": 10.00
        }
        
        response = client.post(
            "/orders/order/add-item/99999",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 404

    def test_add_item_to_other_user_order(self, client, user_token, test_db):
        """Test that user cannot add items to another user's order"""
        # Create another user's order
        from app.models.tables import User, Order
        from app.main import bcrypt_context
        
        other_user = User(
            email="other@example.com",
            username="otheruser",
            password=bcrypt_context.hash("pass123"),
            active=True,
            admin=False
        )
        test_db.add(other_user)
        test_db.commit()
        test_db.refresh(other_user)
        
        other_order = Order(user_id=other_user.id)
        test_db.add(other_order)
        test_db.commit()
        test_db.refresh(other_order)
        
        headers = {"Authorization": f"Bearer {user_token}"}
        payload = {
            "quantity": 1,
            "flavor": "Test",
            "size": "Medium",
            "unit_price": 10.00
        }
        
        response = client.post(
            f"/orders/order/add-item/{other_order.id}",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 403

    def test_remove_item_from_order(self, client, user_token, sample_order_with_items, test_db):
        """Test removing item from order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Get first item ID
        item_id = sample_order_with_items.items[0].id
        
        response = client.post(
            f"/orders/order/remove-item/{item_id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Item successfully removed" in data["message"]
        assert "quantity_items_ordered" in data

    def test_remove_nonexistent_item(self, client, user_token):
        """Test removing non-existent item"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.post(
            "/orders/order/remove-item/99999",
            headers=headers
        )
        
        assert response.status_code == 404

    def test_visualize_order(self, client, user_token, sample_order_with_items):
        """Test viewing order details"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.get(
            f"/orders/order/{sample_order_with_items.id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "quantity_items_ordered" in data
        assert "order" in data

    def test_visualize_nonexistent_order(self, client, user_token):
        """Test viewing non-existent order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.get("/orders/order/99999", headers=headers)
        
        assert response.status_code == 404

    def test_visualize_other_user_order(self, client, user_token, test_db):
        """Test that user cannot view another user's order"""
        from app.models.tables import User, Order
        from app.main import bcrypt_context
        
        other_user = User(
            email="another@example.com",
            username="anotheruser",
            password=bcrypt_context.hash("pass123"),
            active=True,
            admin=False
        )
        test_db.add(other_user)
        test_db.commit()
        test_db.refresh(other_user)
        
        other_order = Order(user_id=other_user.id)
        test_db.add(other_order)
        test_db.commit()
        test_db.refresh(other_order)
        
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get(f"/orders/order/{other_order.id}", headers=headers)
        
        assert response.status_code == 403

    def test_cancel_order(self, client, user_token, sample_order, test_db):
        """Test canceling order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.post(
            f"/orders/order/cancel/{sample_order.id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "successfully canceled" in data["message"]
        assert data["order"]["status"] == "CANCELED"

    def test_cancel_nonexistent_order(self, client, user_token):
        """Test canceling non-existent order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.post("/orders/order/cancel/99999", headers=headers)
        
        assert response.status_code == 404

    def test_finish_order(self, client, user_token, sample_order, test_db):
        """Test finishing order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.post(
            f"/orders/order/finish/{sample_order.id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "successfully finished" in data["message"]
        assert data["order"]["status"] == "FINISHED"

    def test_finish_nonexistent_order(self, client, user_token):
        """Test finishing non-existent order"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        response = client.post("/orders/order/finish/99999", headers=headers)
        
        assert response.status_code == 404

    def test_admin_can_manage_any_order(self, client, admin_token, sample_order, test_db):
        """Test that admin can manage any order"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Admin should be able to view
        response = client.get(f"/orders/order/{sample_order.id}", headers=headers)
        assert response.status_code == 200
        
        # Admin should be able to cancel
        response = client.post(f"/orders/order/cancel/{sample_order.id}", headers=headers)
        assert response.status_code == 200


@pytest.mark.unit
class TestOrderPriceCalculation:
    """Test order price calculation logic"""

    def test_calculate_price_empty_order(self, test_db, sample_user):
        """Test price calculation for empty order"""
        from app.models.tables import Order
        
        order = Order(user_id=sample_user.id)
        test_db.add(order)
        test_db.commit()
        
        order.calculate_price()
        assert order.price == 0.0

    def test_calculate_price_with_items(self, test_db, sample_order):
        """Test price calculation with items"""
        from app.models.tables import OrderItem
        
        item1 = OrderItem(2, "Pepperoni", "Large", 15.99, sample_order.id)
        item2 = OrderItem(1, "Margherita", "Medium", 12.99, sample_order.id)
        
        test_db.add(item1)
        test_db.add(item2)
        test_db.commit()
        test_db.refresh(sample_order)
        
        sample_order.calculate_price()
        
        expected_price = (2 * 15.99) + (1 * 12.99)
        assert sample_order.price == expected_price

