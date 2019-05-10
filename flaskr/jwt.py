from flask import(Blueprint,g,jsonify,request,redirect,url_for)
from flaskr.createDB import (get_db,close_db)
import pymysql
import jwt,time
from . import myConfig
from functools import wraps

bp=Blueprint('jwt',__name__)

class tokenFeature():
    #使用staticmethod装饰器，这个函数就可以在未实例化类的时候调用
    @staticmethod
    def encode_token(user_id):
        try:
            payload={
                'iss':'LMS',
                'exp':int(time.time())+86400,
                'user_id':user_id
            }
            #time.time()是当前的时间戳，86400是一天的秒数
            qumingzi=jwt.encode(
                payload,
                myConfig.SECRET_KEY,
                algorithm='HS256'
            )
            return qumingzi
        except Exception as e:
            return e
    #本方法用于计算token，exp是过期时间，iss为token签发者
    #Attention!这个qumingzi是b'xxxxxxxxx'这样的，b'和最后的'是多余的
    @staticmethod
    def decode_token(token_to_decode):
        try:
            payload=jwt.decode(
                token_to_decode,
                myConfig.SECRET_KEY,
                algorithm='HS256'
            )
            return payload
        except jwt.ExpiredSignatureError:
            return 'token已过期'
        except jwt.InvalidTokenError:
            return '无效token'
        except Exception as e:
            return e
    #同理，这个就是解密token获取payload的了...
    def get_encoded(self,user_id):
        return self.encode_token(user_id)
    #这个token内容是一个长长的字符串
    def get_decoded(self,token_to_decode):
        return self.decode_token(token_to_decode)
    #payload是一个字典，所以要转为json后再返回
    #4.25更新：不转为json了，直接返回字典方便取值

#验证身份的装饰器
def login_required(func):
    @wraps(func)
    #保留源信息，本质是endpoint装饰，否则修改函数名很危险
    #上面这个对wraps(func)的注释我自己也不懂...
    def wrapper(*args,**kwargs):
        isExist=request.headers.get('Authorization')
        if isExist!=None:
            token_to_decode=isExist
            payload_content=tokenFeature.get_decoded(tokenFeature,token_to_decode)
            if payload_content=="无效token":
                return redirect(url_for('jwt.errorPort'))
            if payload_content=='token已过期':
                return payload_content
        else:
            return 'http请求错误，请检查requestHeader'
        return func(*args,**kwargs)
    return wrapper

@bp.route('/getToken',methods=('POST',))
def token_to_lms():
    user_id=request.form['user_id']
    token_content=tokenFeature.get_encoded(tokenFeature,user_id)
    return token_content

@bp.route('/testToken',methods=('GET','POST'))
@login_required
def my_token_test():
    token_content=request.headers['Authorization']
    payload_content=tokenFeature.get_decoded(tokenFeature,token_content)
    return jsonify(payload_content)

@bp.route('/errorPort')
def errorPort():
    return '校验失败，请重新登录'



#题外话。token的内容应该是可以客户端修改的吧，那黑客修改之后我们可以识别出来吗？
#他只能修改payload部分，emmmm可以，
#他如果动了payload，我们只需要与解析signature获得的payload做个对比就行了
