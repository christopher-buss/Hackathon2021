import uuid
import connection
from connection import Item


def add_receipt(receipt_name, items, receipt_total):
    current_id = uuid.uuid1()
    session = connection.connect()

    temp_items = [Item(item["name"], item["price"]) for item in items]

    session.execute(
        """
        INSERT INTO receipts (id, name, receipt_items, total)
        VALUES (%s, %s, %s, %s)
        """,
        (current_id, receipt_name, temp_items, receipt_total)
    )
    return current_id


def retrieve_receipt(receipt_id):
    session = connection.connect()
    query = "SELECT name, total, receipt_items FROM receipts WHERE id=" + receipt_id
    print(query)
    res = session.execute(query)
    return res.all()
