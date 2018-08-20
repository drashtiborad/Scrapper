import MySQLdb

from config import MYSQL_DB, MYSQL_HOST, MYSQL_PASS, MYSQL_USER


def connect_sql():
    global db
    try:
        db = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB)
    except Exception as e:
        db = None
    return db


def execute(query, values=None):
    if 'db' not in globals():
        connect_sql()
    if db:
        cursor = db.cursor()
        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            if query.lower().startswith('select'):
                return cursor.fetchall()
            db.commit()
            print("Executed Successfully!!")
        except Exception as f:
            db.rollback()
            print f
    else:
        for i in range(5):
            connect_sql()
            if db:
                break
        if db:
            execute(query, values)
        else:
            print("Unable to connect to mysql")
