from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

#同样，需要添加装饰器；测试阶段暂时不加

#url_prefix会添加到本蓝图下所有url前面
bp=Blueprint('details',__name__,url_prefix='/details')


@bp.route('/det_progress',methods=('POST',))
# @login_required
def def_progress():
    account=request.form['account']
    course_id=request.form['course_id']
    #因为学生在某门课程下的进度，应该是每个教学元素有一组数据，所以应该是list的形式
    progress_det={
        'result':'success',
        'progress_det':()
    }
    cursor=get_db().cursor()

    try:
        cursor.execute(
            'SELECT learning_progress.name,resource.unit_name,learning_progress.progress'
            ' FROM learning_progress,resource'
            ' WHERE learning_progress.resource_id=resource.resource_id'
            ' AND learning_progress.account= %s AND learning_progress.course_id= %s',(account,course_id)
        )
        columnName=(('studentName','unitName','progress'), )
        #把元组的形式写成( (), )就可以把这个columnName做一个完整的元组加进去了
        progress_det['progress_det']+=columnName
        progress_det['progress_det']+=cursor.fetchall()
        return jsonify(progress_det)
    #无解无解，数据库查询操作出来的结果一定是（'201630610496','黄基峰'，'....'...)这样的元组
    #没法给它改成键值对的形式
    except Exception as e:
        progress_det['result']='fail'
        return jsonify(progress_det)

#展示个人下载的所有资源库东西
@bp.route('/det_materials',methods=('POST',))
@login_required
def det_materials():
    account=request.form['account']
    course_id=request.form['course_id']
    materials_det={
        'result':'success',
        'materials_det':[]
    }
    cursor=get_db().cursor()

    try:
        cursor.execute(
            'SELECT materials_id,materials_name FROM download_materials'
            ' WHERE account=%s AND course_id=%s',(account,course_id)
        )
        materials_down=cursor.fetchall()
        for i in materials_down:
            each_mat={
                'materials_id':i[0],
                'materials_name':i[1]
            }
            materials_det['materials_det'].append(each_mat)
    except Exception as e:
        raise
    return jsonify(materials_det)

#展示个人下载的所有辅导材料
@bp.route('/det_guidance',methods=('POST',))
@login_required
def det_guidance():
    account=request.form['account']
    course_id=request.form['course_id']
    guidance_det={
        'result':'success',
        'guidance_det':[]
    }
    cursor=get_db().cursor()

    try:
        cursor.execute(
            'SELECT guidance_id,guidance_name FROM download_guidance'
            ' WHERE account=%s AND course_id=%s',(account,course_id)
        )
        guidance_down=cursor.fetchall()
        for i in guidance_down:
            each_gui={
                'guidance_id':i[0],
                'guidance_name':i[1]
            }
            guidance_det['guidance_det'].append(each_gui)
    except Exception as e:
        raise
    return jsonify(guidance_det)

#根据需求返回所有内容...
@bp.route('/listAll',methods=('POST',))
@login_required
def listAll():
    account=request.form['account']
    course_id=request.form['course_id']
    homework_id=request.form['homework_id']
    cursor=get_db().cursor()
    listAll_res={
        'result':"success",
        'userId':"",
        'userName':"",
        'individualBehavior':{
            'submitTime':"",
            'progress':[],
            'discussionCnt':[],
            'materialsCnt':[],
            'guidanceCnt':[],
            'discussionRecord':[],
            'downloadRecord':[]
        }
    }

    #part0 获取作业提交时间
    try:
        cursor.execute(
            'SELECT submit_time FROM homeworkTime'
            ' WHERE account=%s AND homework_id=%s',(account,homework_id)
        )
        submitTime=cursor.fetchall()
        submitTime=submitTime[0][0]
        listAll_res['individualBehavior']['submitTime']=submitTime
    except Exception as e:
        raise

    #part1 获取个人本课程的学习进度，顺便把名字放到response里
    # try:
    #     cursor.execute(
    #         'SELECT COUNT(DISTINCT unit_id) FROM learning_progress'
    #         ' WHERE account=%s AND course_id=%s',(account,course_id)
    #     )
    #     totalUnit=cursor.fetchall()
    #     totalUnit=totalUnit[0][0]
    #     #不对，怎么获取某一天的...
    #     cursor.execute(
    #         'SELECT MIN(name),unit_id,MAX(progress) FROM learning_progress'
    #         ' WHERE account=%s AND course_id=%s'
    #         ' GROUP BY unit_id',(account,course_id)
    #     )
    #
    # except Exception as e:
    #     raise

    #获取资源下载情况


    get_db().commit()

    return jsonify(listAll_res)
