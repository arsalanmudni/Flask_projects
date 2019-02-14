from datetime import datetime
from flaskr import db

class User(db.Document):
    username = db.StringField()
    email = db.StringField()
    contact = db.StringField()

    def __repr__(self):
        return "User Info : name : {}, email : {} contact : {}".format(self.username,self.email,self.contact)

# class User(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(30),unique=True , nullable=False)
#     email = db.Column(db.String(40),nullable=False)
#
#     def __repr__(self):
#         return "User : username : {}, email : {} )".format(self.username,self.email)
#
# class Post(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(50),nullable=False)
#     created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
#     content = db.Column(db.Text)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     def __repr__(self):
#
#         return "Post : title : {} posted_at : {} ".format(self.title,str(self.created_at))
#
# class Domains(db.Model):
#     __bind_key__ = 'domain'
#     id = db.Column(db.Integer,primary_key=True)
#     domain_name = db.Column(db.String(100),unique=True,nullable=False)
#     domain_status = db.Column(db.Integer,default=-1)
#
#     def __repr__(self):
#
#         return "Domain : name {} status : {}".format(self.domain_name,self.domain_status)