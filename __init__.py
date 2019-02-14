from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mudni:ars123@localhost/flask'
app.config['SQLALCHEMY_BINDS'] = {'domain' : 'mysql://mudni:ars123@localhost/domain'}
db = SQLAlchemy(app)