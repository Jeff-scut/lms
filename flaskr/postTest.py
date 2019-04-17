from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql

bp=Blueprint('postTest',__name__)

@bp.route('/postHere',methods=('GET','POST'))
def handle():
    cursor=get_db().cursor()
    if request.method=='POST':
        aaa=request.form['aaa']
        bbb=request.form['bbb']
        try:
            cursor.execute('INSERT INTO user VALUES(?,?,?)',(aaa,bbb,"666"))
            get_db().commit()
        except:
            get_db().rollback()

        close_db()
        return jsonify('hhh')
    return 'nssb'
