from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

bp=Blueprint('score',__name__)


@bp.route('/getScore',methods=('GET','POST'))
def getResource():
    account=request.form['account']
    course_id=request.form['course_id']
    #分数
    score={
        'activeScore':0,
        'homeworkScore':0
    }

    cursor=get_db().cursor()
    cursor.execute(
        'select * from resource'
        )
    data=cursor.fetchall()


    #下载材料活跃分
    cursor.execute(
        'select * from download_materials where account=%s',account
        )
    download_data=cursor.fetchall()
    for i in range(len(download_data)):
        #下载暂定计两分
        score['activeScore'] += 2

    #讨论活跃分
    cursor.execute(
        'select * from discussion'
        )
    discussion_data=cursor.fetchall()
    for i in range(len(discussion_data)):
        #讨论暂定算一分
        score['activeScore']+=1

    #进度活跃分
    cursor.execute(
        'select progress from learning_progress'
        )
    progress_data=cursor.fetchall()
    #progress_data[i][6]表示进度百分比
    for i in range(len(progress_data)):
        #活跃度算分，暂定为进度百分比*5
        score['activeScore'] += eval(progress_data[i])*5

    #作业分计算
    # cursor.execute(
    #     'select * from homework '
    #     '   where course_id=%s and section_id=%s and account=%s',(course_id,section_id,account)
    # )




    return jsonify(score)
