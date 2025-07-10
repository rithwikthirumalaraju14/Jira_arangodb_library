Jira ArangoDB Connector
A Python library to migrate Jira issues, including comments and attachments, to an ArangoDB database.
Installation
Install the package using pip:
pip install jira_arangodb_connector

Or, install from source:
git clone https://github.com/rithwikt2003/jira_arangodb_connector.git
cd jira_arangodb_connector
pip install .

Requirements

Python 3.6+
requests>=2.28.0
python-arango>=7.3.0

Usage
from jira_arangodb_connector import JiraArangoConnector

jira_config = {
    "email": "your_email@example.com",
    "api_token": "your_api_token",
    "domain": "your_domain.atlassian.net"
}

arango_config = {
    "url": "http://localhost:8529",
    "username": "root",
    "password": "your_password",
    "database": "jira_db",
    "collection": "jira_issues"
}

connector = JiraArangoConnector(jira_config, arango_config)
connector.migrate_issues()

Testing
Run unit tests using pytest:
pip install pytest
pytest tests/

License
This project is licensed under the MIT License - see the LICENSE file for details.