from django.db import connection, transaction


def getMaxCustomerId():
    cursor = connection.cursor()
    query = 'SELECT MAX(cusId) FROM customer'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def insertCustomer(params):
    cursor = connection.cursor()
    query = "INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()


def updateCustomer(params):
    cursor = connection.cursor()
    query = "UPDATE customer SET firstName=%s, lastName=%s, contactNo=%s, zipcode=%s, streetName=%s, cExpDate=%s, cSerialNo=%s WHERE cusId=%s"
    cursor.execute(query, params)
    transaction.commit_unless_managed()


def validateCustomer(params):
    cursor = connection.cursor()
    query = "SELECT count(*) FROM customer WHERE email=%s AND password=%s"
    cursor.execute(query, params)
    return True if cursor.fetchone()[0] == 1 else False


def getCustIdByUserId(id):
    cursor = connection.cursor()
    query = "SELECT cusId FROM customer where user_id=%s"
    cursor.execute(query, [id])
    return cursor.fetchone()[0]


def getCustInfoById(id):
    cursor = connection.cursor()
    query = "SELECT * FROM customer where cusId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row


def getCustByEmail(email):
    cursor = connection.cursor()
    query = "SELECT count(*) FROM customer where email=%s"
    cursor.execute(query, [email])
    return True if cursor.fetchone()[0] == 1 else False