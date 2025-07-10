from jira_arangodb_connector import JiraArangoConnector

jira_config = {
    "email": "example@gmail.com",
    "api_token": "",  # Replace with your actual token
    "domain": "example.atlassian.net"
}

arango_config = {
    "url": "http://localhost:8529",
    "username": "root",
    "password": "",
    "database": "new",
    "collection": "jira_issues"
}

connector = JiraArangoConnector(jira_config, arango_config)
connector.migrate_issues()
