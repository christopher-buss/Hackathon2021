import uuid
import connection


def add_receipt(receipt_name, receipt_splits, receipt_total):
    current_id = uuid.uuid1()
    session = connection.connect()
    session.execute(
        """
        INSERT INTO Receipts (id, name, splits, total)
        VALUES (%s, %s, %s, %s)
        """,
        (current_id, receipt_name, receipt_splits, receipt_total)
    )
    return current_id


def retrieve_receipt(receipt_id):
    session = connection.connect()
    return session.execute(("SELECT name, items, total, splits FROM Receipts WHERE id=" + receipt_id))
