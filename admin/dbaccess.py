from django.db import connection, transaction

cursor = connection.cursor()


def getMaxCompanyId():
    query = 'SELECT MAX(coyId) FROM Company'
    cursor.execute(query)
    return cursor.fetchone()[0] if not None else 0


def insertCompany(params):
    query = "INSERT INTO Company VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def getMaxDriverId():
    query = 'SELECT MAX(driverId) FROM Driver'
    cursor.execute(query)
    return cursor.fetchone()[0] if not None else 0
