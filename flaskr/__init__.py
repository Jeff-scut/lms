import os
from flask import Flask
from . import download_materials

def create_app(test_config=None):
    app=Flask(__name__)

    app.register_blueprint(download_materials.bp)
    # 蓝图的注册

    from . import postTest
    app.register_blueprint(postTest.bp)

    return app
