from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

user_name = 'chat_app_user'
password = '12345'

# change default user and password
auth_provider = PlainTextAuthProvider(username='cassandra',
                                      password='cassandra')
cluster = Cluster(auth_provider=auth_provider)
session = cluster.connect()

session.execute(
    f"CREATE ROLE IF NOT EXISTS {user_name} WITH PASSWORD = '{password}' AND SUPERUSER = true AND LOGIN = true;")

cluster.shutdown()


# create keyspace and tables
auth_provider = PlainTextAuthProvider(username=user_name,
                                      password=password)
cluster = Cluster(auth_provider=auth_provider)
session = cluster.connect()

with open('tables.cql') as f:
    session.execute(f"DROP ROLE IF EXISTS 'cassandra';")
    commands = f.read().split(';')
    for command in commands:
        command = command.replace('\n', '')
        print(command)
        session.execute(command)
