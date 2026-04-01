"""Unit tests for main application"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'src'))

from main import app

@pytest.fixture
def client():
    return TestClient(app)

class TestHealth:
    """Health check endpoint tests"""
    
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_readiness_check(self, client):
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"
    
    def test_liveness_check(self, client):
        response = client.get("/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

class TestRoot:
    """Root endpoint tests"""
    
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

class TestItems:
    """Items endpoint tests"""
    
    def test_list_items_empty(self, client):
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
    
    def test_create_item(self, client):
        item = {
            "name": "Test Item",
            "description": "A test item",
            "price": 9.99
        }
        response = client.post("/items", json=item)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["price"] == 9.99
        assert "id" in data
    
    def test_create_and_list_items(self, client):
        # Create item
        item = {"name": "Item 1", "description": "Test", "price": 10.0}
        response = client.post("/items", json=item)
        assert response.status_code == 200
        
        # List items
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
    
    def test_get_item(self, client):
        # Create item
        item = {"name": "Get Item", "description": "Test", "price": 15.0}
        response = client.post("/items", json=item)
        item_id = response.json()["id"]
        
        # Get item
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Get Item"
    
    def test_get_nonexistent_item(self, client):
        response = client.get("/items/9999")
        assert response.status_code == 404
    
    def test_update_item(self, client):
        # Create item
        item = {"name": "Original", "description": "Test", "price": 20.0}
        response = client.post("/items", json=item)
        item_id = response.json()["id"]
        
        # Update item
        updated_item = {"name": "Updated", "description": "Modified", "price": 25.0}
        response = client.put(f"/items/{item_id}", json=updated_item)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["price"] == 25.0
    
    def test_delete_item(self, client):
        # Create item
        item = {"name": "Delete Me", "description": "Test", "price": 5.0}
        response = client.post("/items", json=item)
        item_id = response.json()["id"]
        
        # Delete item
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify deleted
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 404

class TestMetrics:
    """Metrics endpoint tests"""
    
    def test_metrics_endpoint(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_items" in data
        assert "app_version" in data
