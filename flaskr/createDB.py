import pymysql
from flask import g

def get_db():
    if 'connect' not in g:
        g.connect=pymysql.connect(
            host="45.32.40.85",
            user="jeff",
            password="password",
            database="lms",
            charset="utf8"
        )
    return g.connect
    # 建立一个到mysql的连接，存储在g中

def close_db():
    connect=g.pop('connect',None)
    if connect is not None:
        connect.close()
    #关闭连接
