# Access to MariaDB database with pymysql

from flask import g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="localhost",
            user="coursetrackr",
            password="vERCERgrOphY",
            database="coursetrackr",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db