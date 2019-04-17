from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql

bp=Blueprint('download_materials',__name__)

@bp.route('/download_materials',methods=('GET','POST'))
def handle():
    cursor=get_db().cursor()
    if request.method=='POST':
        account=request.form['account']
        name=request.form['name']
        course_id=request.form['course_id']
        materials_id=request.form['materials_id']
        materials_name=request.form['materials_name']
        try:
            cursor.execute(
                'INSERT INTO user VALUES(?,?,?,?,?)',
                (account,name,course_id,materials_id,materials_name)
            )
            get_db().commit()
        except:
            get_db().rollback()
        close_db()
        return jsonify('插入成功')
    return '这是一个GET不是POST'
