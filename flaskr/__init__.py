from flask import Flask
from . import collector
from . import jwt
from . import myConfig
from . import score
from . import details
from . import compare
from . import common
from flask_cors import *


def create_app(test_config=None):
    app=Flask(__name__)
    CORS(app,supports_credentials=True)

    app.config.from_object(myConfig)

    app.register_blueprint(jwt.bp)
    app.register_blueprint(collector.bp)
    app.register_blueprint(score.bp)
    app.register_blueprint(details.bp)
    app.register_blueprint(compare.bp)
    app.register_blueprint(common.bp)
    # 蓝图的注册

    return app
