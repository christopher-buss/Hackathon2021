from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table
import connection


class Receipts(Model):
    id = columns.UUID(primary_key=True)
    name = columns.Text()
    receipt_items = columns.List(value_type=columns.Text)
    total = columns.Double()
    splits = columns.List(value_type=columns.Text)


session = connection.connect()
session.sync_table(Receipts)
