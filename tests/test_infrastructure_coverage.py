import pytest
from unittest.mock import MagicMock, patch
from src.database import DatabaseClient
from src.repositories.vehicle_repository import VehicleRepository
from bson import ObjectId

# --- DatabaseClient Tests ---

def test_database_client_singleton():
    """Test that get_db_client returns the same instance"""
    from src.database import get_db_client, db_client
    assert get_db_client() is db_client

def test_database_connection_lifecycle():
    """Test connect and close methods"""
    client = DatabaseClient()
    
    with patch("src.database.MongoClient") as mock_mongo:
        # Test Connect
        client.connect()
        mock_mongo.assert_called_once()
        assert client.client is not None
        assert client.db is not None
        
        # Test Get Collection (should reuse connection)
        col = client.get_collection("test_col")
        assert col is not None
        
        # Test Close
        client.close()
        assert client.client is None
        client.client_instance = None # reset for safety if needed

def test_database_reconnect_on_get_collection():
    """Test that get_collection connects if not connected"""
    client = DatabaseClient()
    client.client = None # Ensure disconnected
    
    with patch("src.database.MongoClient") as mock_mongo:
        client.get_collection("test_col")
        mock_mongo.assert_called_once()
        assert client.client is not None

# --- VehicleRepository Tests (Edge Cases) ---

def test_repo_get_by_id_invalid_object_id():
    """Test get_by_id with invalid ObjectId string"""
    repo = VehicleRepository()
    result = repo.get_by_id("invalid-id")
    assert result is None

def test_repo_get_by_id_not_found():
    """Test get_by_id when document doesn't exist"""
    repo = VehicleRepository()
    with patch.object(repo, 'get_collection') as mock_get_col:
        mock_get_col.return_value.find_one.return_value = None
        result = repo.get_by_id("507f1f77bcf86cd799439011")
        assert result is None

def test_repo_update_invalid_id():
    """Test update with invalid ObjectId"""
    repo = VehicleRepository()
    result = repo.update("invalid-id", {})
    assert result is None

def test_repo_delete_invalid_id():
    """Test delete with invalid ObjectId"""
    repo = VehicleRepository()
    result = repo.delete("invalid-id")
    assert result is False

def test_repo_delete_not_found():
    """Test delete when document doesn't exist"""
    repo = VehicleRepository()
    with patch.object(repo, 'get_collection') as mock_get_col:
        mock_get_col.return_value.delete_one.return_value.deleted_count = 0
        result = repo.delete("507f1f77bcf86cd799439011")
        assert result is False

def test_repo_list_vehicles_mapping():
    """Test list_vehicles handles _id conversion correctly"""
    repo = VehicleRepository()
    mock_cursor = [
        {"_id": ObjectId("507f1f77bcf86cd799439011"), "data": "v1"},
        {"_id": ObjectId("507f1f77bcf86cd799439012"), "data": "v2"}
    ]
    
    with patch.object(repo, 'get_collection') as mock_get_col:
        mock_get_col.return_value.find.return_value.skip.return_value.limit.return_value = mock_cursor
        
        results = repo.list_vehicles(10, 0)
        
        assert len(results) == 2
        assert results[0]["_id"] == "507f1f77bcf86cd799439011"
        assert results[1]["_id"] == "507f1f77bcf86cd799439012"
