from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required
import datetime

#同样，需要添加装饰器；测试阶段暂时不加

#url_prefix会添加到本蓝图下所有url前面
bp=Blueprint('details',__name__,url_prefix='/details')

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
    get_db().commit()
    close_db()
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
    get_db().commit()
    close_db()
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
            'discussionRecord':[]
        }
    }

    # 首先验证有没有输错，如果没有记录就结束本次查询
    try:
        cursor.execute(
            'SELECT COUNT(*) FROM learning_progress'
            ' WHERE account=%s AND course_id=%s',(account,course_id)
        )
        aaa=cursor.fetchall()
        if aaa[0][0]==0:
            return '无相应记录,请检查帐号是否输错'
    except Exception as e:
        raise

    #获取作业提交时间
    try:
        cursor.execute(
            'SELECT submit_time FROM homeworkTime'
            ' WHERE account=%s AND homework_id=%s',(account,homework_id)
        )
        submitTime=cursor.fetchall()
        if submitTime==():
            submitTime="ERROR"
        else:
            submitTime=str(submitTime[0][0])
        listAll_res['individualBehavior']['submitTime']=submitTime
    except Exception as e:
        raise

    #资源库下载次数
    try:
        cursor.execute(
            'SELECT COUNT(materials_id),create_time FROM download_materials'
            ' WHERE account=%s AND course_id=%s'
            ' GROUP BY create_time',(account,course_id)
        )
        aaa=cursor.fetchall()
        for i in aaa:
            axiba={
                'count':i[0],
                'date':str(i[1].date())
            }
            listAll_res['individualBehavior']['materialsCnt'].append(axiba)
    except Exception as e:
        raise

    #辅导材料下载次数
    try:
        cursor.execute(
            'SELECT COUNT(guidance_id),create_time FROM download_guidance'
            ' WHERE account=%s AND course_id=%s'
            ' GROUP BY create_time',(account,course_id)
        )
        aaa=cursor.fetchall()
        for i in aaa:
            jiuminga={
                'count':i[0],
                'date':str(i[1].date())
            }
            listAll_res['individualBehavior']['guidanceCnt'].append(jiuminga)
    except Exception as e:
        raise

    #讨论参与次数
    try:
        #通过这次开发，感觉写sql语句的能力得到了不少锻炼...顺便发掘了一下format的用法
        cursor.execute(
            'SELECT COUNT(DISTINCT discussion_id),DATE_FORMAT(create_time,"%Y-%m-%d") FROM discussion'
            ' WHERE account={0} AND course_id={1}'
            ' GROUP BY DATE_FORMAT(create_time,"%Y-%m-%d")'.format(account,course_id)
        )
        aaa=cursor.fetchall()
        for i in aaa:
            yaolewoba={
                'count':i[0],
                'date':i[1]
            }
            listAll_res['individualBehavior']['discussionCnt'].append(yaolewoba)
    except Exception as e:
        raise

    #列出讨论的详细记录
    try:
        cursor.execute(
            'SELECT post_id,content,create_time FROM discussion'
            ' WHERE account={} AND course_id={}'.format(account,course_id)
        )
        aaa=cursor.fetchall()
        if aaa==():
            listAll_res['individualBehavior']['discussionRecord'].append('没有讨论记录')
        else:
            for i in aaa:
                xinqingbianhao={
                    'type':"",
                    'time':str(i[2].date()),
                    'content':i[1],
                    'zhu_conten':""
                }
                if i[0]=='NULL':
                    xinqingbianhao['type']="发起讨论"
                else:
                    xinqingbianhao['type']='回复'
                    cursor.execute(
                        'SELECT DISTINCT content FROM discussion'
                        ' WHERE discussion_id=%s',i[0]
                    )#为什么这里在试图用{}.format的时候会报错？暂时不管...
                    bbb=cursor.fetchall()
                    xinqingbianhao['zhu_conten']=bbb[0][0]
                listAll_res['individualBehavior']['discussionRecord'].append(xinqingbianhao)
    except Exception as e:
        raise

    #获取在这门课程的所有章节的目前进度
    try:
        cursor.execute(
            'SELECT MIN(learning_progress.name),MIN(resource.unit_name),MAX(learning_progress.progress)'
            ' FROM learning_progress,resource'
            ' WHERE learning_progress.resource_id=resource.resource_id'
            ' AND learning_progress.account=%s AND learning_progress.course_id=%s'
            ' GROUP BY learning_progress.unit_id',(account,course_id)
        )#又采用了group by之后用min取名字的写法...先不管了，先能用再说..
        aaa=cursor.fetchall()
        for i in aaa:
            kuaiwanle={
                'unit_name':i[1],
                'progress':i[2]
            }
            listAll_res['individualBehavior']['progress'].append(kuaiwanle)
    except Exception as e:
        raise

    get_db().commit()
    close_db()
    return jsonify(listAll_res)
