from django.db import connection, transaction


def getMaxCompanyId():
    cursor = connection.cursor()
    query = 'SELECT MAX(coyId) FROM Company'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def insertCompany(params):
    cursor = connection.cursor()
    query = "INSERT INTO Company VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def getMaxDriverId():
    cursor = connection.cursor()
    query = 'SELECT MAX(driverId) FROM Driver'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def insertDriver(params):
    cursor = connection.cursor()
    query = "INSERT INTO Driver VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def insertVehicle(params):
    cursor = connection.cursor()
    query = "INSERT INTO Vehicle VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def insertCar(params):
    cursor = connection.cursor()
    query = "INSERT INTO CAR VALUES (%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def insertBus(params):
    cursor = connection.cursor()
    query = "INSERT INTO BUS VALUES (%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def insertLorry(params):
    cursor = connection.cursor()
    query = "INSERT INTO LORRY VALUES (%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]