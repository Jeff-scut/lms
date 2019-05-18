from flask import(Blueprint,g,jsonify,request,make_response)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required
import time

format="%Y-%m-%d %H:%M:%S"

bp=Blueprint('collector',__name__)


def formatTime(t):
    return time.strftime(format,t)


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
        create_time=request.form['create_time']
        try:
            value = [account, name, course_id, materials_id, materials_name, create_time]
            cursor.execute(
                'SELECT COUNT(*) FROM download_materials WHERE account=%s AND materials_id=%s',(account,materials_id)
            )
            isExist=cursor.fetchall()
            #首先检查是否存在这个人对这个material的下载记录
            if isExist[0][0]!=None:
                if isExist[0][0]==0:
                    cursor.execute(
                        'INSERT INTO download_materials (account,name,course_id,materials_id,materials_name,create_time)'
                        ' VALUES(%s,%s,%s,%s,%s,%s)',value
                        )
                else:
                    return jsonify('记录已存在')
            else:
                return jsonify('非法数据')
            #如果是none，是查询出错，可能是非法数据引起的；
            #如果是0就说明这是一条新纪录，执行insert操作；非0则说明已有记录
            #下面的接口也是类似这样的处理
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
            cursor.execute('SELECT COUNT(*) FROM materials WHERE materials_id=%s',materials_id)
            isExist=cursor.fetchall()
            if isExist[0][0]!=None:
                if isExist[0][0]==0:
                    cursor.execute(
                        'INSERT INTO materials (course_id,materials_id,materials_name)'
                        ' VALUES(%s,%s,%s)',value
                    )
                else:
                    return jsonify('记录已存在')
            else:
                return jsonify('非法数据')
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
    credit_weight=0.3
    if request.method=='POST':
        account=request.form['account']
        username=request.form['name']
        course_id = request.form['course_id']
        unit_id = request.form['unit_id']
        resource_id = request.form['resource_id']
        resource_type=request.form['resource_type']
        #视频实际播放时长
        cur_time = request.form['current_time']
        #视频总时长
        duration=request.form['duration']
        #进度最大为1.0
        progress='0'
        if not (int(cur_time) and int(duration)):
            return jsonify({
                'result':'failed',
                'message':'操作失败'
            })
        if int(cur_time)/int(duration) <1.0:
            progress=str(round(int(cur_time)/int(duration),2))
        else:
            progress="1.0"
        create_time=request.form['create_time']
        credit=str(int(duration)*credit_weight)
        try:
            value = (
                account,
                username,
                course_id,
                unit_id,
                resource_id,
                resource_type,
                cur_time,
                duration,
                progress,
                credit,
                create_time
            )
            cursor.execute(
                'INSERT INTO learning_progress (account,name,course_id,unit_id,resource_id,resource_type,cur_time,duration,progress,credit,create_time) VALUES'
                '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value
            )#我还是把learning_progress表的name字段名字改回来了...因为其他好多写完的语句是用了name，不想改了！
            get_db().commit()
        except Exception as e:
            get_db().rollback()
            print(e)
            return jsonify({
            'result':'failed',
            'message':'操作失败'
            })
        get_db().close()

        return jsonify({
            'result':'success',
            'message':'操作完成'
        })
    return '本API只接受POST请求'


@bp.route('/resource',methods=('POST',))
@login_required
def resource():
    cursor=get_db().cursor()
    if request.method=='POST':
        course_id = request.form['course_id']
        unit_id = request.form['unit_id']
        unit_name=request.form['unit_name']
        resource_id = request.form['resource_id']
        resource_type=request.form['resource_type']
        try:
            value = [course_id,unit_id,unit_name,resource_id,resource_type]
            cursor.execute(
                'SELECT COUNT(*) FROM resource WHERE unit_id=%s and resource_type=%s '
                ,(unit_id,resource_type)
            )
            isExist=cursor.fetchall()
            if isExist!=None:
                if isExist[0][0]==0:
                    cursor.execute(
                        'INSERT INTO resource (course_id,unit_id,unit_name,resource_id,resource_type)'
                        'VALUES(%s,%s,%s,%s,%s)',value
                        )
                else:
                    cursor.execute(
                        'UPDATE resource SET resource_id=%s WHERE unit_id=%s AND resource_type=%s '
                        ,(resource_id,unit_id,resource_type)
                    )
            else:
                return jsonify('非法数据')
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
        create_time=request.form['create_time']
        #重要提醒：如果是一个这是发起帖，前端构造requestBody的时候要把post_id设置成'NULL'
        #补充：没有对重复帖子做过滤，但是前端控制好正常也不会有重复的情况出现吧。。
        try:
            value = [account,name,course_id,discussion_id,post_id,content,create_time]
            cursor.execute(
                'INSERT INTO discussion (account,name,course_id,discussion_id,post_id,content,create_time)'
                ' VALUES(%s,%s,%s,%s,%s,%s,%s)',value
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
        guidance_id=request.form['guidance_id']
        guidance_name=request.form['guidance_name']
        try:
            value=[course_id,unit_id,guidance_id,guidance_name]
            #检查本unit是否已有辅导资料
            cursor.execute(
                'SELECT COUNT(*) FROM guidance WHERE course_id=%s AND unit_id=%s',(course_id,unit_id)
            )
            tempVal=cursor.fetchall()
            if tempVal[0][0]!=None:
                if tempVal[0][0]==0:
                    cursor.execute(
                        'INSERT INTO guidance (course_id,unit_id,guidance_id,guidance_name)'
                        ' VALUES (%s,%s,%s,%s)',value
                    )
                else:
                    cursor.execute(
                        'UPDATE guidance SET guidance_id=%s,guidance_name=%s'
                        ' WHERE course_id=%s AND unit_id=%s',(guidance_id,guidance_name,course_id,unit_id)
                    )
            else:
                return jsonify('非法数据')
            get_db().commit()
        except Exception as e:
            get_db().rollback()
            return jsonify('数据插入失败')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/download_guidance',methods=('POST',))
@login_required
def download_guidance():
    cursor=get_db().cursor()
    if request.method=='POST':
        account=request.form['account']
        name=request.form['name']
        course_id=request.form['course_id']
        unit_id=request.form['unit_id']
        guidance_id=request.form['guidance_id']
        guidance_name=request.form['guidance_name']
        create_time=request.form['create_time']
        try:
            value=[account,name,course_id,unit_id,guidance_id,guidance_name,create_time]
            cursor.execute(
                'INSERT INTO download_guidance'
                ' VALUES (%s,%s,%s,%s,%s,%s,%s)',value
            )
            get_db().commit()
        except Exception as e:
            get_db().rollback()
            return jsonify('数据插入失败，此条已记录')
        close_db()
        return jsonify('操作完成')
    return '本API只接受POST请求'


@bp.route('/homeworkTime',methods=('POST',))
@login_required
def homeworkTime():
    cursor=get_db().cursor()
    if request.method=='POST':
        account=request.form['account']
        name=request.form['name']
        course_id=request.form['course_id']
        homework_id=request.form['homework_id']
        submit_time=request.form['submit_time']
        try:
            value=(account,name,course_id,homework_id,submit_time)
            cursor.execute(
                'INSERT INTO homeworkTime (account,name,course_id,homework_id,submit_time) VALUES'
                '(%s,%s,%s,%s,%s)',value
            )
            get_db().commit()
        except Exception as e:
            get_db().rollback()
            return jsonify({
                'result':'failed',
                'message':'操作失败'
            })
        get_db().close()
        return jsonify({
             'result':'success',
            'message':'操作成功'
        })


@bp.route('/getCurrentTime',methods=('GET',))
@login_required
def getCurrentTime():
    cursor=get_db().cursor()
    if request.method=='GET':
        account=request.args['account']
        resource_id=request.args['resource_id']
        cursor.execute(
            'SELECT resource_id,cur_time FROM learning_progress WHERE account=%s AND resource_id=%s',
            (account,resource_id)
        )
        data=cursor.fetchall()
        current_time=0
        if data:
            current_time=data[-1][1]
        return jsonify({
            'result':'success',
            'resource_id':resource_id,
            'current_time':current_time
        })
