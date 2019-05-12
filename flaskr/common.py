from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

bp=Blueprint('common',__name__,url_prefix='/common')

#返回课程资源库所有资源的id和名字
@bp.route('/materials',methods=('POST',))
@login_required
def com_mat():
    course_id=request.form['course_id']
    cursor=get_db().cursor()
    res_mat={
        'result':'success',
        'materials':[]
    }
    cursor.execute(
        'SELECT materials_id,materials_name FROM materials'
        ' WHERE course_id=%s',course_id
    )
    get_db().commit()
    materials=cursor.fetchall()
    for i in materials:
        each_mat={
            'materials_id':i[0],
            'materials_name':i[1]
        }
        res_mat['materials'].append(each_mat)
    close_db()
    return jsonify(res_mat)

#同上..变成辅导材料而已
@bp.route('/guidance',methods=('POST',))
@login_required
def com_gui():
    course_id=request.form['course_id']
    cursor=get_db().cursor()
    res_gui={
        'result':'success',
        'guidance':[]
    }
    cursor.execute(
        'SELECT guidance_id,guidance_name FROM guidance'
        ' WHERE course_id=%s',course_id
    )
    get_db().commit()
    guidance=cursor.fetchall()
    for i in guidance:
        each_gui={
            'guidance_id':i[0],
            'guidance_name':i[1]
        }
        res_gui['guidance'].append(each_gui)
    close_db()
    return jsonify(res_gui)
