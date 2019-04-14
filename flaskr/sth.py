from flask import(Blueprint,flash,g,redirect,render_template,request,session,url_for)
from flaskr.createDB import get_db
import pymysql

bp=Blueprint('sth',__name__)

@bp.route('/hello')
def showHello():
    cursor=get_db().cursor()
    try:
        cursor.execute('INSERT INTO courses values ("wc","nm",6,0,"fuck")')
        get_db().commit()
    except:
        get_db().rollback()
    return render_template('hello.html')
