import pytest
import requests
from unittest.mock import patch
from jira_arangodb_connector.jira_client import JiraClient

@pytest.fixture
def jira_client():
    return JiraClient(email="test@example.com", api_token="test_token", domain="test.atlassian.net")

@patch('requests.get')
def test_check_projects_success(mock_get, jira_client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"values": [{"id": "1", "name": "Test Project"}]}
    projects = jira_client.check_projects()
    assert len(projects) == 1
    assert projects[0]["name"] == "Test Project"

@patch('requests.get')
def test_check_projects_failure(mock_get, jira_client):
    mock_get.return_value.status_code = 403
    mock_get.return_value.text = "Forbidden"
    with pytest.raises(Exception, match="Failed to fetch projects: 403 Forbidden"):
        jira_client.check_projects()