from django.db import connection, transaction


def getMaxJobId():
    cursor = connection.cursor()
    query = 'SELECT MAX(jobId) FROM Job'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getMaxTripId():
    cursor = connection.cursor()
    query = 'SELECT MAX(tripId) FROM Trip'
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def insertJob(params):
    cursor = connection.cursor()
    query = "INSERT INTO Job VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def insertTrip(params):
    cursor = connection.cursor()
    query = "INSERT INTO Trip VALUES (%s,TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'),TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'),%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def insertReqResource(params):
    cursor = connection.cursor()
    query = "INSERT INTO reqResource VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, params)
    transaction.commit_unless_managed()
    return params[0]


def searchCompanies(coyNameArray, streetNameArray):
    cursor = connection.cursor()
    query = "SELECT * FROM company WHERE "

    if coyNameArray:
        query += "(coyName LIKE "
        for x in coyNameArray:
            query += "'%s' OR coyName LIKE " % (x)
        query = query[:-18] + "') AND "

    if streetNameArray:
        query += "(streetName LIKE "
        for x in streetNameArray:
            query += "'%s' OR streetName LIKE " % (x)
        query = query[:-21] + "') AND "

    query = query[:-5]
    companyResult = cursor.execute(query)
    return companyResult


def getAvailableCars(params):
    cursor = connection.cursor()
    query = "SELECT v.carplateNo, v.transType, v.drivingClass " \
            "FROM vehicle v WHERE v.carplateNo IN (SELECT table1.carplateNo FROM " \
            "(SELECT rRr.carplateNo AS carplateNo, COUNT(rRr.carplateNo) AS count " \
            "FROM reqResource rRr " \
            "GROUP BY rRr.carplateNo) table1, " \
            "(SELECT rR.carplateNo AS carplateNo, COUNT(rR.carplateNo) AS count " \
            "FROM vehicle v, car c, reqResource rR, trip t " \
            "WHERE v.vehType = %s " \
            "AND c.category = %s " \
            "AND v.coyId = %s " \
            "AND v.carplateNo = c.carplateNo " \
            "AND v.carplateNo = rR.carplateNo " \
            "AND rR.tripId = t.tripId " \
            "AND((t.startTime > TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS')) OR (t.endTime < TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'))) " \
            "GROUP BY rR.carplateNo) table2 " \
            "WHERE table1.carplateNo = table2.carplateNo " \
            "AND table1.count = table2.count " \
            "UNION " \
            "SELECT v.carplateNo " \
            "FROM vehicle v, car c " \
            "WHERE v.vehType = %s " \
            "AND c.category = %s " \
            "AND v.coyId = %s " \
            "AND v.carplateNo = c.carplateNo " \
            "AND v.carplateNo NOT IN(SELECT DISTINCT(rR.carplateNo)FROM reqResource rR)) " \
            "ORDER BY v.drivingClass DESC;"
    cursor.execute(query, params)
    return cursor.fetchall()


def getAvailableBuses(params):
    cursor = connection.cursor()
    query = "SELECT v.carplateNo, v.transType, v.drivingClass " \
            "FROM vehicle v WHERE v.carplateNo IN (SELECT table1.carplateNo FROM " \
            "(SELECT rRr.carplateNo AS carplateNo, COUNT(rRr.carplateNo) AS count " \
            "FROM reqResource rRr " \
            "GROUP BY rRr.carplateNo) table1, " \
            "(SELECT rR.carplateNo AS carplateNo, COUNT(rR.carplateNo) AS count " \
            "FROM vehicle v, bus b, reqResource rR, trip t " \
            "WHERE v.vehType = %s " \
            "AND b.category = %s " \
            "AND v.coyId = %s " \
            "AND v.carplateNo = b.carplateNo " \
            "AND v.carplateNo = rR.carplateNo " \
            "AND rR.tripId = t.tripId " \
            "AND((t.startTime > TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS')) OR (t.endTime < TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'))) " \
            "GROUP BY rR.carplateNo) table2 " \
            "WHERE table1.carplateNo = table2.carplateNo " \
            "AND table1.count = table2.count " \
            "UNION " \
            "SELECT v.carplateNo " \
            "FROM vehicle v, bus b " \
            "WHERE v.vehType = %s " \
            "AND b.category = %s " \
            "AND v.coyId = %s " \
            "AND v.carplateNo = b.carplateNo " \
            "AND v.carplateNo NOT IN(SELECT DISTINCT(rR.carplateNo)FROM reqResource rR)) " \
            "ORDER BY v.drivingClass DESC;"
    cursor.execute(query, params)
    return cursor.fetchall()


def getAvailableLorries(params):
    cursor = connection.cursor()
    query = "SELECT v.carplateNo, v.transType, v.drivingClass " \
            "FROM vehicle v WHERE v.carplateNo IN (SELECT table1.carplateNo FROM " \
            "(SELECT rRr.carplateNo AS carplateNo, COUNT(rRr.carplateNo) AS count " \
            "FROM reqResource rRr " \
            "GROUP BY rRr.carplateNo) table1, " \
            "(SELECT rR.carplateNo AS carplateNo, COUNT(rR.carplateNo) AS count " \
            "FROM vehicle v, lorry l, reqResource rR, trip t " \
            "WHERE v.vehType = %s " \
            "AND l.tons = %s " \
            "AND v.coyId = %s " \
            "AND v.carplateNo = l.carplateNo " \
            "AND v.carplateNo = rR.carplateNo " \
            "AND rR.tripId = t.tripId " \
            "AND((t.startTime > TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS')) OR (t.endTime < TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'))) " \
            "GROUP BY rR.carplateNo) table2 " \
            "WHERE table1.carplateNo = table2.carplateNo " \
            "AND table1.count = table2.count " \
            "UNION " \
            "SELECT v.carplateNo " \
            "FROM vehicle v, lorry l " \
            "WHERE v.vehType = %s " \
            "AND l.tons = %s " \
            "AND v.coyId = %s " \
            "AND v.carplateNo = l.carplateNo " \
            "AND v.carplateNo NOT IN(SELECT DISTINCT(rR.carplateNo)FROM reqResource rR)) " \
            "ORDER BY v.drivingClass ASC;"
    cursor.execute(query, params)
    return cursor.fetchall()

def getAvailableDrivers(params):
    cursor = connection.cursor()
    query = "SELECT d.driverId, d.drivingClass " \
            "FROM driver d " \
            "WHERE d.driverId IN (SELECT table1.driverId FROM " \
            "(SELECT rRr.driverId AS driverId, COUNT(rRr.driverId) AS count " \
            "FROM reqResource rRr " \
            "GROUP BY rRr.driverId) table1, " \
            "(SELECT rR.driverId AS driverId, COUNT(rR.driverId) AS count " \
            "FROM driver d, reqResource rR, trip t " \
            "WHERE d.coyId = %s " \
            "AND d.driverId = rR.driverId " \
            "AND rR.tripId = t.tripId " \
            "AND((t.startTime > TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS')) OR (t.endTime < TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'))) " \
            "GROUP BY rR.driverId) table2 " \
            "WHERE table1.driverId = table2.driverId " \
            "AND table1.count = table2.count " \
            "UNION " \
            "SELECT d.driverId " \
            "FROM driver d " \
            "WHERE d.coyId = %s " \
            "AND d.driverId NOT IN(SELECT DISTINCT(rR.driverId) FROM reqResource rR));"
    cursor.execute(query, params)
    return cursor.fetchall()


def getAllJobsByCusId(id):
    cursor = connection.cursor()
    query = "SELECT * FROM job WHERE cusId=%s"
    cursor.execute(query, [id])
    return cursor.fetchall()


def getAllTripsByJobId(id):
    cursor = connection.cursor()
    query = "SELECT * FROM trip WHERE jobId=%s"
    cursor.execute(query, [id])
    return cursor.fetchall()


def deleteTrip(id):
    cursor = connection.cursor()
    query = "DELETE FROM trip WHERE tripId=%s"
    cursor.execute(query, [id])
    transaction.commit_unless_managed()


def getJobOfTrip(id):
    cursor = connection.cursor()
    query = "SELECT jobId FROM trip WHERE tripId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getDrivingClassOfDriver(id):
    cursor = connection.cursor()
    query = "SELECT drivingClass FROM driver WHERE driverId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getCoyOfTrip(id):
    cursor = connection.cursor()
    query = "SELECT coyId FROM reqResource WHERE tripId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getTripDetails(id):
    cursor = connection.cursor()
    query = "SELECT * FROM trip WHERE tripId=%s"
    cursor.execute(query, [id])
    return cursor.fetchall()


def getReqResourceByTripId(id):
    cursor = connection.cursor()
    query = "SELECT * FROM reqResource WHERE tripId=%s"
    cursor.execute(query, [id])
    return cursor.fetchall()


def deleteJob(id):
    cursor = connection.cursor()
    query = "DELETE FROM job WHERE jobId=%s"
    cursor.execute(query, [id])
    transaction.commit_unless_managed()


def getNoOfCarsByCarplateNos(params):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM car WHERE category=%s AND carplateNo IN (SELECT carplateNo FROM reqResource WHERE tripId=%s)"
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getNoOfBusesByCarplateNos(params):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM bus WHERE category=%s AND carplateNo IN (SELECT carplateNo FROM reqResource WHERE tripId=%s)"
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def getNoOfLorriesByCarplateNos(params):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM lorry WHERE tons=%s AND carplateNo IN (SELECT carplateNo FROM reqResource WHERE tripId=%s)"
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0


def checkTimingClash(params):
    cursor = connection.cursor()
    query = "select DISTINCT(rr.driverId) " \
            "from reqResource rr, trip t " \
            "where rr.tripId = t.tripId " \
            "AND t.tripId <> %s " \
            "AND rr.driverId = %s " \
            "AND (t.startTime >= TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS') AND t.startTime < TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS') " \
            "OR t.startTime <= TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS') AND t.endTime >= TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS') " \
            "OR t.endTime < TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS') AND t.endTime>= TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS')" \
            "OR t.startTime >= TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS') AND t.endTime <= TO_DATE(%s,'DD-MM-YYYY HH24:MI:SS'))"
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row[0] if row is not None else 0


def getListOfCarsByCategoryAndTripIdByDrivingClass(params):
    cursor = connection.cursor()
    query = "SELECT rr.carplateNo, rr.driverId " \
            "FROM reqResource rr, vehicle v, car c " \
            "WHERE rr.carplateNo = v.carplateNo " \
            "AND v.carplateNo = c.carplateNo " \
            "AND c.category = %s " \
            "AND rr.tripId = %s " \
            "ORDER BY v.drivingClass DESC"
    cursor.execute(query, params)
    return cursor.fetchall()


def getListOfBusesByCategoryAndTripIdByDrivingClass(params):
    cursor = connection.cursor()
    query = "SELECT rr.carplateNo, rr.driverId " \
            "FROM reqResource rr, vehicle v, bus b " \
            "WHERE rr.carplateNo = v.carplateNo " \
            "AND v.carplateNo = b.carplateNo " \
            "AND b.category = %s " \
            "AND rr.tripId = %s " \
            "ORDER BY v.drivingClass DESC"
    cursor.execute(query, params)
    return cursor.fetchall()


def getListOfLorriesByTonsAndTripIdByDrivingClass(params):
    cursor = connection.cursor()
    query = "SELECT rr.carplateNo, rr.driverId " \
            "FROM reqResource rr, vehicle v, lorry l " \
            "WHERE rr.carplateNo = v.carplateNo " \
            "AND v.carplateNo = l.carplateNo " \
            "AND l.tons = %s " \
            "AND rr.tripId = %s " \
            "ORDER BY v.drivingClass ASC"
    cursor.execute(query, params)
    return cursor.fetchall()


