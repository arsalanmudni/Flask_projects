import os

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
app = Flask(__name__,instance_relative_config=True)
app.config['MONGOALCHEMY_DATABASE'] = 'tasks'
app.config['SECRET_KEY'] = "this is my key!"
db = MongoAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mudni:ars123@localhost/flask'
# app.config['SQLALCHEMY_BINDS'] = {'domain' : 'mysql://mudni:ars123@localhost/domain'}
# db = SQLAlchemy(app)

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )
#     app.config['MYSQL_DATABASE_USER'] = 'mudni'
#     app.config['MYSQL_DATABASE_PASSWORD'] = 'mud123'
#     app.config['MYSQL_DATABASE_DB'] = 'flask'
#     app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#
#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)
#
#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
#     # a simple page that says hello
#     @app.route('/test/')
#     def hello():
#         return 'Hello, World!'
#
#     return app
