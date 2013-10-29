from django.db import connection


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