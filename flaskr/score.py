from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
from  flaskr.jwt import login_required
import math

bp=Blueprint('score',__name__)

#下面的每个都应该添加装饰器

#传入学生ID和课程ID，返回嫌疑分数
'''
抄袭者判定指标：
    活跃分：课程进度 | 辅导资料下载 | 资源库下载 | 发帖和回帖
    其它：作业提交时间
'''
@bp.route('/getScore',methods=('POST',))
@login_required
def getScore():
    cursor=get_db().cursor()
    if request.method=='POST':
        accounts=request.form['accounts'].split(',')
        course_id=request.form['course_id']
        homework_id=request.form['homework_id']
        scoreResult={
            'result':'success',
            'score':[],
            'message':''
        }
        scores=[]
        timeList=[]
        base_w=50.
        susp_const=2000.
        for account in accounts:
            progress_fullScore = progress_score = guidance_score = discussion_score = materials_score = 0
            #作业提交时间
            try:
                cursor.execute(
                    'SELECT submit_time FROM homeworkTime WHERE account=%s AND homework_id=%s',
                    (account,homework_id)
                )
            except Exception as e:
                print("作业提交时间查询出错")
                print(e)

            data=cursor.fetchone()
            if data:
                submit_time=data[0]
                timeList.append({'account':account,'submit_time':submit_time})
            score={
                'account':account,
                'sbt_score':0.,
                'act_score':0.
            }

            #课程进度得分
            #（进度*本视频价值）求和
            try:
                cursor.execute(
                'SELECT credit,progress FROM learning_progress'
                ' WHERE course_id= %s AND account= %s',(course_id,account)
                )
                #这个目前没法直接取到maxProgress，要在插入时直接更新
                progress_data=cursor.fetchall()
                #progress_data是tuple
                for i in progress_data:
                    progress_score += (float(i[0])*float(i[1]))
            except Exception as e:
                print("课程进度得分查询出错，详细信息：")
                print(e)

            #辅导资料得分
            #假定每下载一个+5分
            try:
                cursor.execute(
                'SELECT COUNT(*) FROM download_guidance'
                ' WHERE account=%s and course_id=%s',(account,course_id)
                )
                guidance_data=cursor.fetchall()
                if guidance_data:
                    guidance_score=guidance_data[0][0]*5.0
            except Exception as e:
                print('辅导资料得分查询出错，详细信息：')
                print(e)

            #资源库下载得分
            #资源库中的文件每项+5分
            try:
                cursor.execute(
                'SELECT COUNT(DISTINCT materials_id) FROM download_materials'
                    ' WHERE account=%s AND course_id=%s',(account,course_id)
                )

                #加了distinct这个参数，重复值就不算
                #其实这个加了也没用..因为建表的时候就设定了主键，不会出现重复的...
                materials_data=cursor.fetchall()
                if materials_data:
                    materials_score=materials_data[0][0]*5.0
            except Exception as e:
                print('资源库得分查询出错，详细信息：')
                print(e)

            #讨论活跃分
            #发起一个新的讨论+5，跟帖+3
            try:
                cursor.execute(
                'SELECT discussion_id,post_id FROM discussion'
                ' WHERE account=%s AND course_id=%s',(account,course_id)
                )
                discussion_data=cursor.fetchall()
                for data in discussion_data:
                    if data[1]=='NULL':
                        discussion_score+=5.0
                    else:
                        discussion_score+=3.0

                    #首先检查discussion_id字段，空则为记录时出错；
                    #跟帖（postid不为空）+1.26，发起帖s's+2.55
            except Exception as e:
                print('讨论得分查询出错，详细信息：')
                print(e)

            #活跃分计算完成
            #5.7修改：分数只由活跃分构成，作为课程总分的一部分
            #计分规则：教师设定4个部分的占比（如50+20+15+15），score=s1*50+s2*20+....
            #s1=actualScore/fullScore s2，3，4同
            #fullScore1可以直接计算credit和，234是人工设定=-=
            try:
                cursor.execute('SELECT credit FROM learning_progress WHERE account= %s AND course_id= %s',(account,course_id))
                all_credit=cursor.fetchall()
                for i in all_credit:
                    progress_fullScore += float(i[0])

                '''cursor.execute('SELECT COUNT(*) FROM guidance WHERE course_id=%s',(course_id,))
                all_guidance=cursor.fetchall()
                guidance_fullScore=all_guidance[0][0]*5.0'''

                '''cursor.execute('SELECT COUNT(*) FROM materials WHERE course_id=%s',(course_id,))
                all_materials=cursor.fetchall()
                materials_fullScore=all_materials[0][0]*5.0'''

                #讨论的总分就直接制定上限了，挺合理的，避免灌水= =..
            except:
                return '查询出错，账号/课程ID输入错误'

            pg_score=progress_score/progress_fullScore if(progress_fullScore) else 0
            active_score=30*(pg_score)+guidance_score+materials_score+discussion_score
            score['act_score']=active_score
            scores.append(score)
        #按作业提交时间降序排序
        #下标越大的元素在以下计算中权值越大
        #即越早提交作业的人权值分越多
        timeList.sort(key=(lambda x:x['submit_time']))
        if timeList:
            w=1
            key={
                'submit_time':timeList[0]['submit_time'],
                'weight':base_w*(1/w) #作业提交时间的权值，按[反比例函数(暂定)]递减
            }
        for i in timeList:
            if i['submit_time']>key['submit_time']:
                #若当前i和key作业提交时间相同，视为同一层次，否则更新到下一个层次
                w+=1
                key['submit_time']=i['submit_time']
                key['weight']=base_w*(1/math.sqrt(w))
            for j in scores:
                if i['account']==j['account']:
                    j['sbt_score']=key['weight'] #永远获取当前层次的权值分

        new_score=[]
        for item in scores:
            total_score=0.
            if item['sbt_score']+item['act_score']:
                #计算总嫌疑值
                total_score=round(susp_const/(item['sbt_score']+item['act_score']),2)
            new_score.append({
                'account':item['account'],
                'suspicionValue':total_score
            })

        scoreResult['score']=new_score
        return jsonify(scoreResult)
