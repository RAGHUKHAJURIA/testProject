"""Smoke tests for deployed application"""
import pytest
import requests
import os

BASE_URL = os.getenv("APP_URL", "http://localhost:8000")

class TestDeployedApp:
    """Smoke tests for deployed application"""
    
    def test_app_is_responding(self):
        """Test if app is responding"""
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_api_endpoints_accessible(self):
        """Test if API endpoints are accessible"""
        response = requests.get(f"{BASE_URL}/", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
    
    def test_items_endpoint_works(self):
        """Test items endpoint"""
        response = requests.get(f"{BASE_URL}/items", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
