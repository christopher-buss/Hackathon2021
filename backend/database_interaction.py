import uuid
import connection
import json


def add_receipt(receipt_name, receipt_items, receipt_total):
    current_id = uuid.uuid1()
    session = connection.connect()
    session.execute(
        """
        INSERT INTO Receipts (id, name, receipt_items, total)
        VALUES (%s, %s, %s)
        """,
        (current_id, receipt_name, receipt_items, receipt_total)
    )
    return current_id


def retrieve_receipt(receipt_id):
    session = connection.connect()
    res = session.execute("SELECT name, total, receipt_items FROM Receipts WHERE id=bc93fc9c-68ab-11eb-9ce7-00155df8e701")
    return res.all()
