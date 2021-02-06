import uuid
import connection
from connection import Item, Split


def add_receipt(receipt_name, items, receipt_total, splits):
    current_id = uuid.uuid1()
    session = connection.connect()

    temp_items = [Item(item["name"], item["price"], item["quantity"]) for item in items]
    test = []
    temp_splits = [Split(split["name"], split["total"], [Item(item["name"], item["price"], item["quantity"]) for item in split['items']]) for split in splits]

    session.execute(
        """
        INSERT INTO receipts (id, name, receipt_items, total, splits)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (current_id, receipt_name, temp_items, receipt_total, temp_splits)
    )
    return current_id


def retrieve_receipt(receipt_id):
    session = connection.connect()
    query = "SELECT name, total, receipt_items, splits FROM receipts WHERE id=" + receipt_id
    print(query)
    res = session.execute(query)
    return res.all()
