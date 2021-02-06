from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask.json import JSONEncoder


class Item(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price


class ItemJSONEncoder(JSONEncoder):
    def default(self, obj):
        if type(obj) == Item:
            return {'name': obj.name, 'price': obj.price}


def connect():
    cloud_config = {
        'secure_connect_bundle': './secure-connect-ReceiptReader.zip'
    }
    auth_provider = PlainTextAuthProvider('hackaway', 'password123')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    cluster.register_user_type('hackaway', 'item', Item)
    session = cluster.connect(keyspace="hackaway")

    row = session.execute("select release_version from system.local").one()
    if row:
        print(row[0])
    else:
        print("An error occurred.")

    return session
