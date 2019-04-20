from flask import(Blueprint,g,jsonify,request)
from flaskr.createDB import (get_db,close_db)
import pymysql
import jwt,time
from . import myConfig

bp=Blueprint('jwt',__name__)

@bp.route('/getToken',methods=('POST',))
def token_to_lms():
    user_id=request.form['user_id']
    token_content=tokenFeature.get_encoded(tokenFeature,user_id)
    payload_content=tokenFeature.get_decoded(tokenFeature,token_content)
    return payload_content
    #这个函数只是测试一下pyjwt功能，结果不错呀
    #后面要把这个函数作为与LMS联系的接口，接收LMS传递的userid，返回token
    #下一步就是做成一个装饰器，在每次请求的时候检查有没有token?

class tokenFeature():
    #使用staticmethod注解，这个函数就可以在未实例化类的时候调用
    @staticmethod
    def encode_token(user_id):
        try:
            payload={
                'iss':'LMS',
                'exp':int(time.time())+86400,
                'user_id':user_id
            }
            qumingzi=jwt.encode(
                payload,
                myConfig.SECRET_KEY,
                algorithm='HS256'
            )
            return qumingzi
        except Exception as e:
            return e
    #本方法用于计算token，exp是过期时间，86400是一天的秒数
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
    #同理，这个就是解密token获取payload的了...
    def get_encoded(self,user_id):
        return self.encode_token(user_id)
    #这个token内容是一个长长的字符串
    def get_decoded(self,token_to_decode):
        return jsonify(self.decode_token(token_to_decode))
    #payload是一个字典，所以要转为json后再返回

#题外话。token的内容应该是可以客户端修改的吧，那黑客修改之后我们可以识别出来吗？
#他只能修改payload部分，emmmm可以，
#他如果动了payload，我们只需要与解析signature获得的payload做个对比就行了
