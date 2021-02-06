from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import connection

connection.connect()

class Receipts(Model):
    id = columns.UUID(primary_key=True)
    name = columns.Text()
    items = columns.List()
    total = columns.Double()
    splits = columns.List()

