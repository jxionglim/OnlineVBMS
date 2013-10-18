from django.db import connection, transaction

cursor = connection.cursor()


def getMaxCustomerId():
    query = 'SELECT MAX(cusId) FROM customer'
    cursor.execute(query)
    return cursor.fetchone()[0] if not None else 0


def insertCustomer(params):
    query = "INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def validateCustomer(params):
    query = "SELECT count(*) FROM customer WHERE email=%s AND password=%s"
    cursor.execute(query, params)
    return True if cursor.fetchone()[0] == 1 else False

