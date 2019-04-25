from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

bp=Blueprint('collector',__name__)

@bp.route('/download_materials',methods=('GET','POST'))
@login_required
def download_materials():
    cursor=get_db().cursor()
    if request.method=='POST':
        account=request.form['account']
        name=request.form['name']
        course_id=request.form['course_id']
        materials_id=request.form['materials_id']
        materials_name=request.form['materials_name']
        try:
            value = [account, name, course_id, materials_id, materials_name]
            try:
                cursor.execute(
                'insert into download_materials values(%s,%s,%s,%s,%s)',value
                )
            except:
                print("error")

            get_db().commit()

        except:
            get_db().rollback()
        close_db()
        return jsonify('插入成功')
    return '这是一个GET不是POST'


@bp.route('/materials',methods=('GET','POST'))
@login_required
def materials():
    cursor=get_db().cursor()
    if request.method=='POST':
        course_id=request.form['course_id']
        materials_id=request.form['materials_id']
        materials_name=request.form['materials_name']
        try:
            value = [course_id, materials_id, materials_name]
            try:
                cursor.execute(
                'insert into materials values(%s,%s,%s)',value
                )
            except:
                print("error")
            get_db().commit()
        except:
            get_db().rollback()
        close_db()
        return jsonify('插入成功')
    return '这是一个GET不是POST'


@bp.route('/learning_progress',methods=('GET','POST'))
@login_required
def learning_progress():
    cursor=get_db().cursor()
    if request.method=='POST':
        account=request.form['account']
        name=request.form['name']
        section_id = request.form['section_id']
        course_id = request.form['course_id']
        unit_id = request.form['unit_id']
        resource_id = request.form['resource_id']
        resource_type=request.form['resource_type']
        progress=request.form['progress']
        try:
            value = [account,name,course_id,section_id,unit_id,resource_id,resource_type,progress]
            try:
                cursor.execute(
                'insert into learning_progress_values(%s,%s,%s,%s,%s,%s,%s,%s)',value
                )
            except:
                print("error")
            get_db().commit()
        except:
            get_db().rollback()
        close_db()
        return jsonify('插入成功')
    return '这是一个GET不是POST'


@bp.route('/resource',methods=('GET','POST'))
@login_required
def resource():
    cursor=get_db().cursor()
    if request.method=='POST':
        section_id = request.form['section_id']
        course_id = request.form['course_id']
        unit_id = request.form['unit_id']
        resource_id = request.form['resource_id']
        resource_type=request.form['resource_type']
        try:
            value = [course_id,section_id,unit_id,resource_id,resource_type]
            try:
                cursor.execute(
                'insert into resource_values(%s,%s,%s,%s,%s)',value
                )
            except:
                print("error")
            get_db().commit()
        except:
            get_db().rollback()
        close_db()
        return jsonify('插入成功')
    return '这是一个GET不是POST'


@bp.route('/discussion',methods=('GET','POST'))
@login_required
def discussion():
    cursor=get_db().cursor()
    if request.method=='POST':
        account = request.form['account']
        name = request.form['name']
        course_id = request.form['course_id']
        discussion_id = request.form['discussion_id']
        post_id=request.form['post_id']
        content=request.form['content']
        try:
            value = [account,name,course_id,discussion_id,post_id,content]
            try:
                cursor.execute(
                'insert into discussion_values(%s,%s,%s,%s,%s,%s)',value
                )
            except:
                print("error")
            get_db().commit()
        except:
            get_db().rollback()
        close_db()
        return jsonify('插入成功')
    return '这是一个GET不是POST'
