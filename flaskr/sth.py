from flask import(Blueprint,g,jsonify)
from flaskr.createDB import (get_db,close_db)
import pymysql

bp=Blueprint('sth',__name__)

@bp.route('/hello')
def showHello():
    cursor=get_db().cursor()
    try:
        cursor.execute('SELECT * FROM BALABALA')
        wcnm = cursor.fetchall()
        get_db().commit()
    except:
        get_db().rollback()
        print("error:反正就是出错了")
    close_db()
    return jsonify(wcnm)
