from django.db import connection, transaction
import datetime


def getMaxCompanyId():
    cursor = connection.cursor()
    query = 'SELECT MAX(coyId) FROM Company'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getMaxDriverId():
    cursor = connection.cursor()
    query = 'SELECT MAX(driverId) FROM Driver'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def checkUniqueEmail(email):
    cursor = connection.cursor()
    query = "SELECT * FROM Company WHERE email=%s"
    cursor.execute(query, [email])
    row = cursor.fetchone()
    return False if row is not None else True


def insertCompany(params):
    cursor = connection.cursor()
    query = "INSERT INTO Company VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def updateCompany(params):
    cursor = connection.cursor()
    query = "UPDATE COMPANY SET coyName=%s, email=%s, faxNo=%s, contactNo=%s, zipcode=%s, streetName=%s WHERE coyId=%s"
    cursor.execute(query, params)
    transaction.commit_unless_managed()


def deleteCompany(id):
    cursor = connection.cursor()
    query = "DELETE FROM COMPANY WHERE coyId=%s"
    cursor.execute(query, [id])
    transaction.commit_unless_managed()


def insertDriver(params):
    cursor = connection.cursor()
    query = "INSERT INTO Driver VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def updateDriver(params):
    cursor = connection.cursor()
    query = "UPDATE DRIVER SET firstName=%s, lastName=%s, contactNo=%s, drivingClass=%s WHERE driverId=%s"
    cursor.execute(query, params)
    transaction.commit_unless_managed()


def deleteDriver(id):
    cursor = connection.cursor()
    query = "DELETE FROM DRIVER WHERE driverId=%s"
    cursor.execute(query, [id])
    transaction.commit_unless_managed()


def checkUniqueCarplateNo(carplateNo):
    cursor = connection.cursor()
    query = "SELECT * FROM Vehicle WHERE carplateNo=%s"
    cursor.execute(query, [carplateNo])
    row = cursor.fetchone()
    return False if row is not None else True


def checkUniqueIuNo(iuNo):
    cursor = connection.cursor()
    query = "SELECT * FROM Vehicle WHERE iuNo=%s"
    cursor.execute(query, [iuNo])
    row = cursor.fetchone()
    return False if row is not None else True


def insertVehicle(params):
    cursor = connection.cursor()
    query = "INSERT INTO Vehicle VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def deleteVehicle(carplateNo):
    cursor = connection.cursor()
    query = "DELETE FROM VEHICLE WHERE carplateNo=%s"
    cursor.execute(query, [carplateNo])
    transaction.commit_unless_managed()


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


def getCompanies():
    cursor = connection.cursor()
    query = 'SELECT * FROM COMPANY'
    cursor.execute(query)
    row = cursor.fetchall()
    return row


def getCompanyById(id):
    cursor = connection.cursor()
    query = "SELECT * FROM COMPANY WHERE coyId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row


def getDriversById(id):
    cursor = connection.cursor()
    query = "SELECT driverId, firstName, lastName, contactNo, drivingClass FROM DRIVER WHERE coyId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchall()
    return row


def getDriverByDid(id):
    cursor = connection.cursor()
    query = "SELECT * FROM DRIVER WHERE driverId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row


def getVehiclesById(id):
    cursor = connection.cursor()
    query = "SELECT carplateNo, iuNo, manufacturer, model, transType, vehType FROM VEHICLE WHERE coyId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchall()
    return row


def getCoyIdByCarplateNo(carplateNo):
    cursor = connection .cursor()
    query = "SELECT coyId FROM VEHICLE WHERE carplateNo=%s"
    cursor.execute(query, [carplateNo])
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getCarsById(id):
    cursor = connection.cursor()
    query = "SELECT v.carplateNo, v.iuNo, v.manufacturer, v.model, v.transType, c.category FROM VEHICLE v, CAR c WHERE v.coyId=%s AND v.carplateNo = c.carplateNo"
    cursor.execute(query, [id])
    row = cursor.fetchall()
    return row


def getBusesById(id):
    cursor = connection.cursor()
    query = "SELECT v.carplateNo, v.iuNo, v.manufacturer, v.model, v.transType, b.category FROM VEHICLE v, BUS b WHERE v.coyId=%s AND v.carplateNo = b.carplateNo"
    cursor.execute(query, [id])
    row = cursor.fetchall()
    return row


def getLorriesById(id):
    cursor = connection.cursor()
    query = "SELECT v.carplateNo, v.iuNo, v.manufacturer, v.model, v.transType, l.tons FROM VEHICLE v, LORRY l WHERE v.coyId=%s AND v.carplateNo = l.carplateNo"
    cursor.execute(query, [id])
    row = cursor.fetchall()
    return row


def getJobs():
    cursor = connection.cursor()
    query = 'SELECT j.jobId, j.dateCreated, j.amount, c.coyId, c.coyName, cs.email, cs.cusId FROM JOB j, COMPANY c, CUSTOMER cs WHERE j.coyId=c.coyId AND j.cusId=cs.cusId'
    cursor.execute(query)
    row = cursor.fetchall()
    return row


def getNumDriByClassByCoy(id):
    cursor = connection.cursor()
    query = "SELECT d.drivingClass, COUNT(driverId) AS numDri " \
            "FROM company c, driver d " \
            "WHERE c.coyId = d.coyId " \
            "AND c.coyId = %s " \
            "GROUP BY c.coyId, d.drivingClass " \
            "ORDER BY d.drivingClass ASC"
    cursor.execute(query, [id])
    rows = cursor.fetchall()
    return rows


def getNumVehByCatByCoy(id):
    cursor = connection.cursor()
    query = "SELECT type, category, numVeh " \
            "FROM " \
                "(SELECT \'Car\' AS type, car.category, COUNT(v.carplateNo) AS numVeh, c.coyId " \
                "FROM vehicle v, car, company c " \
                "WHERE v.carplateNo = car.carplateNo " \
                "AND v.coyId = c.coyId " \
                "GROUP BY car.category, c.coyId " \
                "UNION " \
                "SELECT \'Bus\' AS type, b.category, COUNT(v.carplateNo) AS numVeh, c.coyId " \
                "FROM vehicle v, bus b, company c " \
                "WHERE v.carplateNo = b.carplateNo " \
                "AND v.coyId = c.coyId " \
                "GROUP BY b.category, c.coyId " \
                "UNION " \
                "SELECT \'Lorry\' AS type, TO_CHAR(l.tons,\'9\') AS category, COUNT(v.carplateNo) AS numVeh, c.coyId " \
                "FROM vehicle v, lorry l, company c " \
                "WHERE v.carplateNo = l.carplateNo " \
                "AND v.coyId = c.coyId GROUP BY l.tons, c.coyId) A " \
            "WHERE A.coyId = %s "
    cursor.execute(query, [id])
    rows = cursor.fetchall()
    return rows


def checkIfCompanyHaveTrips(id):
    now = datetime.datetime.now()
    cursor = connection.cursor()
    query = "SELECT * FROM COMPANY c WHERE EXISTS (SELECT * FROM REQRESOURCE r, TRIP t WHERE c.coyId=r.coyId AND t.tripId=r.tripId AND %s > t.endTime and c.coyId=%s)"
    cursor.execute(query,[now,id])
    row = cursor.fetchone()
    return False if row is not None else True


def checkIfDriverHaveTrips(id):
    now = datetime.datetime.now()
    cursor = connection.cursor()
    query = "SELECT * FROM DRIVER d WHERE EXISTS (SELECT * FROM REQRESOURCE r, TRIP t WHERE d.driverId=r.driverId AND t.tripId=r.tripId AND %s > t.endTime and d.driverId=%s)"
    cursor.execute(query,[now,id])
    row = cursor.fetchone()
    return False if row is not None else True


def checkIfVehicleHaveTrips(carplateNo):
    now = datetime.datetime.now()
    cursor = connection.cursor()
    query = "SELECT * FROM VEHICLE v WHERE EXISTS (SELECT * FROM REQRESOURCE r, TRIP t WHERE v.carplateNo=r.carplateNo AND t.tripId=r.tripId AND %s > t.endTime and v.carplateNo=%s)"
    cursor.execute(query,[now,carplateNo])
    row = cursor.fetchone()
    return False if row is not None else True