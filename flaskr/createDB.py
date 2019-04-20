import pymysql
from flask import (g,current_app)

def get_db():
    if 'connect' not in g:
        g.connect=pymysql.connect(
            host=current_app.config['DBHOST'],
            user=current_app.config["USER"],
            password=current_app.config['PASSWORD'],
            database=current_app.config['DATABASE'],
            charset=current_app.config['CHARSET']
        )
    return g.connect
    # 建立一个到mysql的连接，存储在g中

def close_db():
    connect=g.pop('connect',None)
    if connect is not None:
        connect.close()
    #关闭连接
