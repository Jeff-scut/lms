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
    #无解无解，数据库查询操作出来的结果一定是（'201630610496','黄基峰'，'....'...)这样的元组
    #没法给它改成键值对的形式
    return jsonify(progress_det)

@bp.route('/det_guidance',methods=('POST',))
#@login_required
def det_guidance():
    cursor=get_db().cursor()
    cursor.execute(
        ''
    )
