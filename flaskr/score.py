from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required

bp=Blueprint('score',__name__)

#下面的每个都应该添加装饰器

#传入学生ID和课程ID，返回嫌疑分数
@bp.route('/getScore',methods=('GET','POST'))
def getResource():
    account=request.form['account']
    course_id=request.form['course_id']
    score={
        'activeScore':0,
        'homeworkScore':0
    }

    cursor=get_db().cursor()

    #课程进度得分
    #（进度*本视频/pdf价值）求和
    try:
        cursor.execute(
        'SELECT credit,progress FROM learning_progress'
        ' WHERE course_id= %s AND account= %s',(course_id,account)
        )
        #这个目前没法直接取到maxProgress，要在这里做逻辑判断/插入时直接更新
        progress_data=cursor.fetchall()
        #progress_data是tuple
        progress_score=0
        for i in progress_data:
            progress_score += (i[0]*float(i[1]))
    except Exception as e:
        print("课程进度得分查询出错，详细信息：")
        print(e)

    #辅导资料得分
    #假定每下载一个+2分
    try:
        cursor.execute(
        'SELECT COUNT(*) FROM guidance'
        ' WHERE account=%s and course_id=%s',(account,course_id)
        )
        guidance_data=cursor.fetchall()
        guidance_score=guidance_data[0][0]*2
    except Exception as e:
        print('辅导资料得分查询出错，详细信息：')
        print(e)

    #资源库下载得分
    #资源库中的文件每项+1.33分
    try:
        cursor.execute(
        'SELECT COUNT(DISTINCT materials_id) FROM download_materials'
        ' WHERE account=%s AND course_id=%s',(account,course_id)
        )
        #加了distinct这个参数，重复值就不算
        #其实这个加了也没用..因为建表的时候就设定了主键，不会出现重复的...
        materials_data=cursor.fetchall()
        materials_score=materials_data[0][0]*1.33
    except Exception as e:
        print('资源库得分查询出错，详细信息：')
        print(e)

    #讨论活跃分
    #发起一个新的讨论+2.55，跟帖+1.26
    try:
        cursor.execute(
        'SELECT discussion_id,post_id,id FROM discussion'
        ' WHERE account=%s AND course_id=%s',(account,course_id)
        )
        discussion_data=cursor.fetchall()
        discussion_score=0
        for j in discussion_data:
            if j[0]!=None:
                if j[1]==None:
                    discussion_score+=2.55
                else:
                    discussion_score+=1.26
            else:
                print("数据有误，请检查此条记录，ID为",(j[2]) )
            #首先检查discussion_id字段，空则为记录时出错；
            #跟帖（postid不为空）+1.26，发起帖+2.55
    except Exception as e:
        print('讨论得分查询出错，详细信息：')
        print(e)

    #活跃分计算完成
    score['activeScore']=progress_score+guidance_score+materials_score+discussion_score

    return jsonify(score)

    #作业分计算
    #获取作业提交时间，根据排名赋分
    # cursor.execute(
    #     'SELECT ? FROM homework'
    # )
