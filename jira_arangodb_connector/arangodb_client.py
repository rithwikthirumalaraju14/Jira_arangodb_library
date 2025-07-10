from arango import ArangoClient

class ArangoDBClient:
    def __init__(self, url, username, password, database, collection):
        self.url = url
        self.username = username
        self.password = password
        self.database = database
        self.collection = collection
        self.client = ArangoClient(hosts=url)
        self.db = None
        self.coll = None

    def connect(self):
        """Connect to ArangoDB and set up database and collection."""
        # Connect to system database to create target database if needed
        sys_db = self.client.db('_system', username=self.username, password=self.password)
        if not sys_db.has_database(self.database):
            sys_db.create_database(self.database)
        self.db = self.client.db(self.database, username=self.username, password=self.password)
        if not self.db.has_collection(self.collection):
            self.db.create_collection(self.collection)
        self.coll = self.db.collection(self.collection)

    def save_issue(self, issue_data):
        """Save an issue to ArangoDB."""
        # Use issue key as the document key to avoid duplicates
        issue_data['_key'] = issue_data['key']
        if self.coll.has(issue_data['_key']):
            self.coll.update(issue_data)
        else:
            self.coll.insert(issue_data)