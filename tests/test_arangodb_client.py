import pytest
from arango import ArangoClient
from unittest.mock import patch
from jira_arangodb_connector.arangodb_client import ArangoDBClient

@pytest.fixture
def arango_client():
    return ArangoDBClient(
        url="http://localhost:8529",
        username="root",
        password="test_password",
        database="test_db",
        collection="test_collection"
    )

@patch.object(ArangoClient, 'db')
def test_connect(mock_db, arango_client):
    mock_sys_db = mock_db.return_value
    mock_sys_db.has_database.return_value = False
    mock_sys_db.create_database.return_value = True
    mock_db.return_value.has_collection.return_value = False
    mock_db.return_value.create_collection.return_value = True
    
    arango_client.connect()
    assert arango_client.db is not None
    assert arango_client.coll is not None