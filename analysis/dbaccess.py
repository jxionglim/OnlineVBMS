from django.db import connection
import datetime


def getJobStartLoc():
    cursor = connection.cursor()
    query = 'SELECT DISTINCT startLocation FROM trip'
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def getJobEndLoc():
    cursor = connection.cursor()
    query = 'SELECT DISTINCT endLocation FROM trip'
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def getAllCompanies():
    cursor = connection.cursor()
    query = 'SELECT DISTINCT coyId, coyName FROM company ORDER BY coyName ASC'
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def getCoyInfoByCoyId(id):
    cursor = connection.cursor()
    query = "SELECT * FROM company WHERE coyId=%s"
    cursor.execute(query, [id])
    row = cursor.fetchone()
    return row


def getTripsByLocation(startLoc, endLoc, qty, period):
    cursor = connection.cursor()
    dateNow = datetime.datetime.now()

    if period == "m":
        deductPeriod = int(qty) * 30
        dateLimit = dateNow - datetime.timedelta(days=deductPeriod)
    elif period == "y":
        deductPeriod = int(qty) * 365
        dateLimit = dateNow - datetime.timedelta(days=deductPeriod)
    else:
        deductPeriod = None

    if deductPeriod is None:
        if startLoc == "a" and endLoc == "e":
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query)
        elif startLoc == "a":
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND LOWER(endLocation) LIKE %s " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, ["%" + endLoc.lower() + "%"])
        elif endLoc == "e":
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND LOWER(startLocation) LIKE %s " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, ["%" + startLoc.lower() + "%"])
        else:
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND LOWER(startLocation) LIKE %s " \
                    "AND LOWER(endLocation) LIKE %s " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, ["%" + startLoc.lower() + "%", "%" + endLoc.lower() + "%"])
    else:
        if startLoc == "a" and endLoc == "e":
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND endTime >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND endTime <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, [dateLimit, dateNow])
        elif startLoc == "a":
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND LOWER(endLocation) LIKE %s " \
                    "AND endTime >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND endTime <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, ["%" + endLoc.lower() + "%", dateLimit, dateNow])
        elif endLoc == "e":
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND LOWER(startLocation) LIKE %s " \
                    "AND endTime >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND endTime <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, ["%" + startLoc.lower() + "%", dateLimit, dateNow])
        else:
            query = "SELECT c.coyId, c.coyName, t.jobId, t.tripId, t.startLocation, t.endLocation, t.startTime, t.endTime, u.email " \
                    "FROM trip t, job j, company c, customer u  " \
                    "WHERE t.jobId = j.jobId " \
                    "AND t.cusId = u.cusId " \
                    "AND j.coyId = c.coyId " \
                    "AND LOWER(startLocation) LIKE %s " \
                    "AND LOWER(endLocation) LIKE %s " \
                    "AND endTime >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND endTime <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "ORDER BY c.coyName, t.jobId ASC"
            cursor.execute(query, ["%" + startLoc.lower() + "%", "%" + endLoc.lower() + "%", dateLimit, dateNow])
    rows = cursor.fetchall()
    return rows

def getJobAmtByCoy(order, qty, period):
    cursor = connection.cursor()
    dateNow = datetime.datetime.now()

    if period == "m":
        deductPeriod = int(qty) * 30
        dateLimit = dateNow - datetime.timedelta(days=deductPeriod)
    elif period == "y":
        deductPeriod = int(qty) * 365
        dateLimit = dateNow - datetime.timedelta(days=deductPeriod)
    else:
        deductPeriod = None

    if deductPeriod is None:
        query = "SELECT company.coyId, company.coyName, A.countJob, (A.countJob/B.totalJob)*100, A.total, (A.total/B.totalSum)*100 " \
                "FROM (SELECT c.coyId, count(j.jobId) AS countJob, SUM(amount) AS total " \
                    "FROM job j, company c " \
                    "WHERE j.coyId = c.coyId " \
                    "GROUP BY j.coyId) A, " \
                    "(SELECT COUNT(jobId) AS totalJob, SUM(amount) AS totalSum " \
                    "FROM job) B, company " \
                "WHERE company.coyId = A.coyId " \
                "ORDER by A.countJob, A.total " + order
        cursor.execute(query)
    else:
        query = "SELECT company.coyId, company.coyName, A.countJob, (A.countJob/B.totalJob)*100, A.total, (A.total/B.totalSum)*100 " \
                "FROM (SELECT c.coyId, count(j.jobId) AS countJob, SUM(amount) AS total " \
                    "FROM job j, company c " \
                    "WHERE j.coyId = c.coyId " \
                    "AND j.dateCreated >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND j.dateCreated <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "GROUP BY j.coyId) A, " \
                    "(SELECT COUNT(jobId) AS totalJob, SUM(amount) AS totalSum " \
                    "FROM job " \
                    "WHERE dateCreated >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND dateCreated <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS')) B, company " \
                "WHERE company.coyId = A.coyId " \
                "ORDER by A.countJob, A.total " + order
        cursor.execute(query, [dateLimit, dateNow, dateLimit, dateNow])
    rows = cursor.fetchall()
    return rows


def getTotalCus():
    cursor = connection.cursor()
    query = "SELECT COUNT(cusId) FROM customer"
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0

def getCusDistribution(order):
    cursor = connection.cursor()
    query = "SELECT c.coyId, c.coyName, (coyCus/totalCus)*100 AS cusPercent, coyCus " \
            "FROM (SELECT coyId, COUNT(DISTINCT(cusId)) AS coyCus " \
                "FROM job " \
                "GROUP BY coyId) A, " \
                "(SELECT COUNT(*) AS totalCus " \
                "FROM customer) B, company c " \
            "WHERE A.coyId = c.coyId ORDER BY cusPercent " + order
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def getJoblessCoy(qty, period):
    cursor = connection.cursor()
    dateNow = datetime.datetime.now()

    if period == "m":
        deductPeriod = int(qty) * 30
        dateLimit = dateNow - datetime.timedelta(days=deductPeriod)
    elif period == "y":
        deductPeriod = int(qty) * 365
        dateLimit = dateNow - datetime.timedelta(days=deductPeriod)
    else:
        deductPeriod = None

    if deductPeriod is None:
        query = "SELECT c.coyId, c.coyName " \
                "FROM company c " \
                "WHERE NOT EXISTS " \
                    "(SELECT * " \
                    "FROM reqResource r " \
                    "WHERE r.coyId = c.coyId) " \
                "ORDER BY c.coyName"
        cursor.execute(query)
    else:
        query ="SELECT c.coyId, c.coyName " \
               "FROM company c " \
               "WHERE NOT EXISTS " \
                    "(SELECT * " \
                    "FROM reqResource r, job j " \
                    "WHERE r.coyId = c.coyId " \
                    "AND r.jobId = j.jobId " \
                    "AND j.dateCreated >= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS') " \
                    "AND j.dateCreated <= TO_DATE(%s,'YYYY-MM-DD HH24:MI:SS')) " \
                "ORDER BY coyName"
        cursor.execute(query, [dateLimit, dateNow])
    rows = cursor.fetchall()
    return rows