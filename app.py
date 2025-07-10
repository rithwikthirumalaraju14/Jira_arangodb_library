from jira_arangodb_connector import JiraArangoConnector

jira_config = {
    "email": "rithwik.t2003@gmail.com",
    "api_token": "ATATT3xFfGF0g4FMmb0Ztzpz-IPWX3IEUx88IhtC5sXAiZR3cW1Qny4eeOCn7C5OIrVevSMDA_klImLUyFUqMVf4baGUI97RTbG0bvNgknFpXlk6pEMtCvRDXh4RIKeDIyIa0SLUAZeOyqY0Lx3brUTqcP05w1s7-qLRN17lcLvOpOGaXa7ThIs=2F6596AB",  # Replace with your actual token
    "domain": "rithwikt2003.atlassian.net"
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