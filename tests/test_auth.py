"""
Authentication endpoint tests
"""
import pytest


@pytest.mark.auth
class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_create_account_success(self, client, test_db):
        """Test successful user registration"""
        payload = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepass123",
            "active": True,
            "admin": False
        }
        response = client.post("/auth/create_account", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "newuser@example.com" in data["message"]

    def test_create_account_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email"""
        payload = {
            "email": "user@example.com",  # Already exists
            "username": "anotheruser",
            "password": "password123",
            "active": True,
            "admin": False
        }
        response = client.post("/auth/create_account", json=payload)
        
        assert response.status_code == 400
        assert "email already exists" in response.json()["detail"]

    def test_login_success(self, client, sample_user):
        """Test successful login"""
        payload = {
            "email": "user@example.com",
            "password": "testpassword123"
        }
        response = client.post("/auth/login", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_email(self, client, test_db):
        """Test login with non-existent email"""
        payload = {
            "email": "nonexistent@example.com",
            "password": "somepassword"
        }
        response = client.post("/auth/login", json=payload)
        
        assert response.status_code == 400
        assert "user not found" in response.json()["detail"]

    def test_login_invalid_password(self, client, sample_user):
        """Test login with wrong password"""
        payload = {
            "email": "user@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=payload)
        
        assert response.status_code == 400
        assert "user not found" in response.json()["detail"]

    def test_login_form_success(self, client, sample_user):
        """Test OAuth2 form login"""
        form_data = {
            "username": "user@example.com",  # OAuth2 uses 'username' field
            "password": "testpassword123"
        }
        response = client.post("/auth/login-form", data=form_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_form_invalid_credentials(self, client, test_db):
        """Test OAuth2 form login with invalid credentials"""
        form_data = {
            "username": "invalid@example.com",
            "password": "wrongpass"
        }
        response = client.post("/auth/login-form", data=form_data)
        
        assert response.status_code == 400

    def test_refresh_token_success(self, client, user_token):
        """Test token refresh with valid token"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/auth/refresh", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = client.get("/auth/refresh", headers=headers)
        
        assert response.status_code == 401
        assert "Invalid access token" in response.json()["detail"]

    def test_refresh_token_missing(self, client):
        """Test token refresh without token"""
        response = client.get("/auth/refresh")
        
        assert response.status_code == 401

    def test_auth_home_endpoint(self, client):
        """Test auth home endpoint"""
        response = client.get("/auth/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["authentication"] == False
