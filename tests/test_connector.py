import pytest
from unittest.mock import patch
from jira_arangodb_connector.connector import JiraArangoConnector

@pytest.fixture
def connector():
    jira_config = {
        "email": "test@example.com",
        "api_token": "test_token",
        "domain": "test.atlassian.net"
    }
    arango_config = {
        "url": "http://localhost:8529",
        "username": "root",
        "password": "test_password",
        "database": "test_db",
        "collection": "test_collection"
    }
    return JiraArangoConnector(jira_config, arango_config)

@patch('jira_arangodb_connector.jira_client.JiraClient.check_projects')
@patch('jira_arangodb_connector.jira_client.JiraClient.fetch_issues')
@patch('jira_arangodb_connector.arangodb_client.ArangoDBClient.connect')
@patch('jira_arangodb_connector.arangodb_client.ArangoDBClient.save_issue')
def test_migrate_issues(mock_save_issue, mock_connect, mock_fetch_issues, mock_check_projects, connector):
    mock_check_projects.return_value = [{"id": "1", "name": "Test Project"}]
    mock_fetch_issues.return_value = [
        {
            "key": "TEST-1",
            "fields": {
                "summary": "Test Issue",
                "status": {"name": "Open"},
                "assignee": None
            }
        }
    ]
    connector.migrate_issues()
    mock_connect.assert_called_once()
    mock_save_issue.assert_called_once()