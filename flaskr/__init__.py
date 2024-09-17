import os

from flask import Flask

def create_app(test_config=None):
    #CREATE AND CONFIGURE APP
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        #LOAD THE INSTANCE CONFIG, IF IT EXISTS, WHEN NOT TESTING
        app.config.from_pyfile('config.py', silent=True)
    else: 
        #LOAD THE TEST CONFIG IF PASSED IN
        app.config.from_mapping(test_config)

    #ENSURE THE INSTANCE FOLDER EXISTS
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #A SIMPLE PAGE THAT SAYS HELLO
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    
    return app