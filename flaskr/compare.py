from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

bp=Blueprint('compare',__name__,url_prefix='/compare')

@bp.route('/allFactors',methods=('POST',))
@login_required
def allFactors():
    course_id=request.form['course_id']
    account=request.form['account']
    homework_id=request.form['homework_id']
    list_acc=account.split(",")
    cursor=get_db().cursor()

    factors_response={
        'result':'success',
        'progress_list':[],
        'others_list':[],
        'homework_list':[]
    }

    for i in list_acc:
        each_progress={
            'account' : i,
            'name' : "",
            'progress' : ""
        }
        each_others={
            'account' : i,
            'name': "",
            'discussionCnt': 0,
            'guidanceCnt': 0,
            'materialsCnt': 0
        }#额..突然发现这个取名有点奇怪each others...本意是每一个人的otherFactors...
        each_homework={
            'account': i,
            'name': "",
            'submitTime': ""
        }

        try:
            #part1 计算总的unit个数
            cursor.execute(
                'SELECT COUNT(DISTINCT unit_id) FROM learning_progress'
                ' WHERE account=%s AND course_id=%s',(i,course_id)
            )
            totalUnit=cursor.fetchall()
            totalUnit=totalUnit[0][0]
            if totalUnit==0:
                factors_response['progress_list'].append(each_progress)
                factors_response['others_list'].append(each_others)
                factors_response['homework_list'].append(each_homework)
                continue
                #使用continue可以跳出本次循环，break则会结束整个for
                #这是为了避免因为帐号不存在而下面除以0报错

            #part2 计算每个unit的进度之和
            #这里为了取name用了个骚办法...因为group by unit_id了不能直接取name，
            #所以用了min让它处于unit_id的作用域内
            cursor.execute(
                'SELECT MIN(name),unit_id,MAX(progress) FROM learning_progress'
                ' WHERE account=%s AND course_id=%s'
                ' GROUP BY unit_id',(i,course_id)
            )
            linshigong=cursor.fetchall()
            totalProgress=0
            for j in linshigong:
                each_progress['name']=j[0]
                totalProgress+=float(j[2])

            #part3 总和/总个数=平均课程进度，然后添加到response中
            finalProgress=totalProgress/totalUnit
            each_progress['progress']=finalProgress

            factors_response['progress_list'].append(each_progress)
        except Exception as e:
            print(e)

        try:
            #part0 获取名字 这里应该在learning_progress表取，
            #因为一个人如果极端一点..可能会没有参与讨论没有下载资料...但是一定会有学习进度...
            cursor.execute(
                'SELECT DISTINCT name FROM learning_progress'
                ' WHERE account=%s AND course_id=%s',(i,course_id)
            )
            yourname=cursor.fetchall()
            if yourname==():
                factors_response['others_list'].append(each_others)
                continue
            else:
                each_others['name']=yourname[0][0]

            #part1 获取讨论次数
            cursor.execute(
                'SELECT COUNT(DISTINCT discussion_id) FROM discussion'
                ' WHERE account=%s AND course_id=%s',(i,course_id)
            )
            discussionCnt=cursor.fetchall()
            each_others['discussionCnt']=discussionCnt[0][0]

            #part2 获取guidance下载次数
            cursor.execute(
                'SELECT COUNT(DISTINCT guidance_id) FROM download_guidance'
                ' WHERE account=%s AND course_id=%s',(i,course_id)
            )
            guidanceCnt=cursor.fetchall()
            each_others['guidanceCnt']=guidanceCnt[0][0]

            #part3 获取materials下载次数
            cursor.execute(
                'SELECT COUNT(DISTINCT materials_id) FROM download_materials'
                ' WHERE account=%s AND course_id=%s',(i,course_id)
            )
            materialsCnt=cursor.fetchall()
            each_others['materialsCnt']=materialsCnt[0][0]

            factors_response['others_list'].append(each_others)
        except Exception as e:
            print(e)

        try:
            cursor.execute(
                'SELECT name,submit_time FROM homeworkTime'
                ' WHERE account=%s AND homework_id=%s',(i,homework_id)
            )
            homework=cursor.fetchall()
            each_homework['name']=homework[0][0]
            each_homework['submitTime']=str(homework[0][1])
            factors_response['homework_list'].append(each_homework)
        except Exception as e:
            print(e)

        get_db().commit()

    close_db()
    return jsonify(factors_response)
