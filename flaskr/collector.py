from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

bp=Blueprint('collector',__name__)

@bp.route('/download_materials',methods=('POST',))
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
            cursor.execute(
                'INSERT INTO download_materials VALUES(%s,%s,%s,%s,%s)',value
                )
            get_db().commit()
        except:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/materials',methods=('POST',))
@login_required
def materials():
    cursor=get_db().cursor()
    if request.method=='POST':
        course_id=request.form['course_id']
        materials_id=request.form['materials_id']
        materials_name=request.form['materials_name']
        try:
            value = [course_id, materials_id, materials_name]
            cursor.execute(
                'INSERT INTO materials VALUES(%s,%s,%s)',value
                )
            get_db().commit()
        except:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/learning_progress',methods=('POST',))
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
        credit=request.form['credit']#前端根据pdf页数/视频时长计算credit
        try:
            value = [account,name,course_id,section_id,unit_id,resource_id,resource_type,progress,credit]
            cursor.execute(
                'SELECT COUNT(*) FROM learning_progress WHERE account=%s AND unit_id=%s',(account,unit_id)
            )
            aa=cursor.fetchall()
            if aa[0][0]!=None:
                if aa[0][0]==0:
                    #INSERT
                    cursor.execute(
                        'INSERT INTO learning_progress (account,name,course_id,section_id,unit_id,resource_id,resource_type,progress,credit)'
                        ' VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',value
                    )
                else:
                    #UPDATE
                    cursor.execute(
                        'UPDATE learning_progress SET progress=%s WHERE account=%s AND unit_id=%s'
                            ,(progress,account,unit_id)
                    )
            else:
                return '非法数据'
            get_db().commit()
        except:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/resource',methods=('POST',))
@login_required
def resource():
    cursor=get_db().cursor()
    if request.method=='POST':
        section_id = request.form['section_id']
        course_id = request.form['course_id']
        unit_id = request.form['unit_id']
        unit_name=request.form['unit_name']
        resource_id = request.form['resource_id']
        resource_type=request.form['resource_type']
        try:
            value = [course_id,section_id,unit_id,unit_name,resource_id,resource_type]
            cursor.execute(
                'INSERT INTO resource VALUES(%s,%s,%s,%s,%s,%s)',value
                )
            get_db().commit()
        except:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/discussion',methods=('POST',))
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
        #重要提醒：如果是一个这是发起帖，前端构造requestBody的时候要把post_id设置成'NULL'
        try:
            value = [account,name,course_id,discussion_id,post_id,content]
            cursor.execute(
                'INSERT INTO discussion (account,name,course_id,discussion_id,post_id,content)'
                ' VALUES(%s,%s,%s,%s,%s,%s)',value
                )
            get_db().commit()
        except:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/guidance',methods=('POST',))
@login_required
def guidance():
    cursor=get_db().cursor()
    if request.method=='POST':
        course_id=request.form['course_id']
        unit_id=request.form['unit_id']
        section_id=request.form['section_id']
        guidance_id=request.form['guidance_id']
        guidance_name=request.form['guidance_name']
        try:
            value=[course_id,unit_id,section_id,guidance_id,guidance_name]
            #检查本unit是否已有辅导资料
            cursor.execute(
                'SELECT COUNT(*) FROM guidance WHERE course_id=%s AND unit_id=%s',(course_id,unit_id)
            )
            tempVal=cursor.fetchall()
            if tempVal[0][0]!=None:
                if tempVal[0][0]==0:
                    cursor.execute(
                        'INSERT INTO guidance (course_id,unit_id,section_id,guidance_id,guidance_name)'
                        ' VALUES (%s,%s,%s,%s,%s)',value
                    )
                else:
                    cursor.execute(
                        'UPDATE guidance SET guidance_id=%s,guidance_name=%s'
                        ' WHERE course_id=%s AND unit_id=%s',(guidance_id,guidance_name,course_id,unit_id)
                    )
            else:
                return '非法数据'
            get_db().commit()
        except Exception as e:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return '操作完成'
    return '本API只接受POST请求'


@bp.route('/download_guidance',methods=('POST',))
@login_required
def download_guidance():
    cursor=get_db().cursor()
    if request.method=='POST':
        account=request.form['account']
        name=request.form['name']
        course_id=request.form['course_id']
        guidance_id=request.form['guidance_id']
        guidance_name=request.form['guidance_name']
        try:
            value=[account,name,course_id,guidance_id,guidance_name]
            cursor.execute(
                'INSERT INTO download_guidance (account,name,course_id,guidance_id,guidance_name)'
                ' VALUES (%s,%s,%s,%s,%s)',value
            )
            get_db().commit()
        except Exception as e:
            get_db().rollback()
            return '数据插入失败，此条已记录'
        close_db()
        return '操作完成'
    return '本API只接受POST请求'

#TODO: 作业记录接口
