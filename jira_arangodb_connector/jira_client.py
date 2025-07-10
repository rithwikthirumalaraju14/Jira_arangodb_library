import requests
from requests.auth import HTTPBasicAuth
import time

class JiraClient:
    def __init__(self, email, api_token, domain):
        self.email = email
        self.api_token = api_token
        self.base_url = f"https://{domain}"
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {"Accept": "application/json"}

    def check_projects(self):
        """Check accessible Jira projects."""
        projects_url = f"{self.base_url}/rest/api/3/project/search"
        response = requests.get(projects_url, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch projects: {response.status_code} {response.text}")
        projects = response.json().get("values", [])
        if not projects:
            raise Exception("No accessible projects found.")
        return projects

    def fetch_issues(self, max_results=100):
        """Fetch issues created in the last 30 days."""
        all_issues = []
        start_at = 0
        while True:
            search_url = f"{self.base_url}/rest/api/3/search"
            params = {
                "jql": "created >= -30d ORDER BY created DESC",
                "maxResults": max_results,
                "startAt": start_at,
                "fields": "summary,status,assignee"
            }
            response = requests.get(search_url, headers=self.headers, params=params, auth=self.auth)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch issues: {response.status_code} {response.text}")
            data = response.json()
            issues = data.get("issues", [])
            all_issues.extend(issues)
            total = data.get("total", 0)
            if start_at + max_results >= total:
                break
            start_at += max_results
            time.sleep(0.5)
        return all_issues

    def fetch_comments(self, issue_key):
        """Fetch comments for a given issue."""
        comment_url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        response = requests.get(comment_url, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            return [f"Failed to fetch comments: {response.status_code}"]
        comments = response.json().get("comments", [])
        return [self._extract_comment_text(c.get("body", {})) for c in comments]

    def fetch_attachments(self, issue_key):
        """Fetch attachments for a given issue."""
        details_url = f"{self.base_url}/rest/api/3/issue/{issue_key}?fields=attachment"
        response = requests.get(details_url, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            return [f"Fetch failed: {response.status_code}"]
        attachments = response.json().get("fields", {}).get("attachment", [])
        return [{"filename": a["filename"], "url": a["content"]} for a in attachments]

    @staticmethod
    def _extract_comment_text(comment_body):
        """Extract text from a comment body."""
        texts = []
        for content_block in comment_body.get("content", []):
            for inner in content_block.get("content", []):
                if inner.get("type") == "text" and "text" in inner:
                    texts.append(inner["text"])
        return " ".join(texts)