import pymysql

from flask import current_app,g

def get_db():
    if 'db' not in g:
        g.db=pymysql.connect("localhost","root","YES","lab_student")
    return g.db
