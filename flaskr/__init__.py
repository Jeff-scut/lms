from flask import Flask
from . import collector


def create_app(test_config=None):
    app=Flask(__name__)

    app.register_blueprint(collector.bp)
    # 蓝图的注册

    @app.route('/hello')
    def hello():
        return 'Hello, World!'



    return app
