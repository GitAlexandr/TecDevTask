from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class DatabaseService:
    def __init__(self, host, port, keyspace, username, password):
        auth_provider = PlainTextAuthProvider(username=username, password=password)

        self.cluster = Cluster(
            contact_points=[host],
            port=port,
            auth_provider=auth_provider
        )

        self.session = self.cluster.connect(keyspace=keyspace)

    def write_data(self, data):
        query = "INSERT INTO people (url, name, html_code) VALUES (%s, %s, %s)"
        self.session.execute(query, (data['url'], data['name'], data['html_code']))


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cluster.shutdown()
