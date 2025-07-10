from .jira_client import JiraClient
from .arangodb_client import ArangoDBClient

class JiraArangoConnector:
    def __init__(self, jira_config, arango_config):
        self.jira_client = JiraClient(
            email=jira_config['email'],
            api_token=jira_config['api_token'],
            domain=jira_config['domain']
        )
        self.arango_client = ArangoDBClient(
            url=arango_config['url'],
            username=arango_config['username'],
            password=arango_config['password'],
            database=arango_config['database'],
            collection=arango_config['collection']
        )

    def migrate_issues(self):
        """Migrate Jira issues to ArangoDB."""
        print("🔍 Checking Jira projects...")
        projects = self.jira_client.check_projects()
        print(f"✅ Found {len(projects)} accessible projects.")

        print("📥 Fetching Jira issues...")
        issues = self.jira_client.fetch_issues()
        print(f"✅ Fetched {len(issues)} issues.")

        print("📤 Saving issues to ArangoDB...")
        self.arango_client.connect()
        for issue in issues:
            key = issue["key"]
            # Handle assignee safely
            assignee_info = issue["fields"].get("assignee")
            assignee = assignee_info.get("displayName", "Unassigned") if assignee_info is not None else "Unassigned"
            
            issue_data = {
                "key": key,
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"],
                "assignee": assignee,
                "comments": [],
                "attachments": []
            }
            # Fetch and add comments
            try:
                issue_data["comments"] = self.jira_client.fetch_comments(key)
            except Exception as e:
                issue_data["comments"] = [f"Error fetching comments: {str(e)}"]
            # Fetch and add attachments
            try:
                issue_data["attachments"] = self.jira_client.fetch_attachments(key)
            except Exception as e:
                issue_data["attachments"] = [f"Error fetching attachments: {str(e)}"]
            # Save to ArangoDB
            self.arango_client.save_issue(issue_data)
        print(f"✅ Migrated {len(issues)} issues to ArangoDB.")