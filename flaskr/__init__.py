import os
from flask import Flask

def create_app(test_config=None):
    app=Flask(__name__)

    from . import sth
    app.register_blueprint(sth.bp)

    from . import postTest
    app.register_blueprint(postTest.bp)

    return app
