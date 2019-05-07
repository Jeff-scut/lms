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
        'progress_det':[]
    }
    cursor=get_db().cursor()
    print(type(progress_det))
    cursor.execute(
        'SELECT * FROM learning_progress'
        ' WHERE account= %s AND course_id= %s',(account,course_id)
    )
    # for i in range(len())
    progress_det['progress_det']=cursor.fetchall()
    print(type(progress_det['progress_det'][0][1]))
    #无解无解，数据库查询操作出来的结果一定是（'201630610496','黄基峰'，'....'...)这样的元组
    #没法给它改成键值对的形式
    return jsonify(progress_det)
