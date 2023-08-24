from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory, Statement


class ScyllaDB:

    def __init__(self,
                 db_username: str,
                 db_password: str,
                 keyspace: str | None = None) -> None:
        self.db_username = db_username
        self.db_password = db_password
        self.keyspace = keyspace

    def connect(self) -> None:
        auth_provider = PlainTextAuthProvider(username=self.db_username,
                                              password=self.db_password)
        self.cluster = Cluster(auth_provider=auth_provider)
        self.session = self.cluster.connect(self.keyspace)
        self.session.row_factory = dict_factory

    def disconnect(self) -> None:
        self.cluster.shutdown()
