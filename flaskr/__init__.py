from flask import Flask
from . import collector
from . import jwt
from . import myConfig
from flask_cors import *


def create_app(test_config=None):
    app=Flask(__name__)
    CORS(app,supports_credentials=True)

    app.config.from_object(myConfig)

    app.register_blueprint(jwt.bp)
    app.register_blueprint(collector.bp)
    # 蓝图的注册

    return app
