
import json
import logging,os
import sys
import json
from flask_simple_crypt import SimpleCrypt
from flask_restful import Resource,Api,reqparse,abort
log_path = os.path.join(os.getenv('HOME'),'flask.log')
formater = '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s[%(process)d]%(funcName)10s: %(message)s'
logger = logging.basicConfig(format=formater,filename='flask.logs',level=logging.DEBUG)
logger = logging.getLogger('Hello')
sys.path.append('../')
from flaskr import app
from flaskr.models import User


api = Api(app)
security = SimpleCrypt()
security.init_app(app)


def encrypt_resp(resp):
    if type(resp) is dict:
        return security.encrypt(json.dumps(resp)).decode()
    else:
        return security.encrypt(resp).decode()


class Task(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=False, location='args')
        self.parser.add_argument('email', required=False, location='args')
        self.parser.add_argument('contact', required=False, location='args')
        self.parser.add_argument('username_update', required=False, location='args')
        self.parser.add_argument('email_update', required=False, location='args')
        self.parser.add_argument('contact_update', required=False, location='args')
        self.args = self.parser.parse_args()

    def process_query(self,query_data):
        records = list(map(lambda x: x, query_data.raw_output()))
        json_list = []

        for data in records:
            tmp = data
            del tmp['_id']
            json_list.append(tmp)
        json_resp = {"data": json_list}

        return json_resp

    def process_req(self,username=None,email=None,contact=None):
        userdata = User.query
        try:
            if username:
                userdata = userdata.filter(User.username == username)
            if email:
                userdata = userdata.filter(User.email == email)
            if contact:
                userdata = userdata.filter(User.contact == contact)
        except Exception as exp:
            logger.error("Unable to process request error {}".format(exp))
        return userdata

    def update_queryset(self,query_set_data,username=None,email=None,contact=None):
        resp = {}
        query_set = query_set_data
        if username:
            query_set = query_set.set(username=username)
        if email:
            query_set = query_set.set(email=email)
        if contact:
            query_set = query_set.set(contact=contact)
        try:
            resp = self.process_query(query_set_data)
            query_set.multi().execute()
            resp["message"] = "update successfull"
        except Exception as e:
            resp["Error"] = "Update failed"
            resp["ErrorMsg"] = e
        return resp

    def get(self):
        # args = self.parser.parse_args()
        args = self.args
        # if not (args['username'] or args['email'] or args['contact']):
        #     userdata =
        #     return {"Error": "Please provide at least one filteration crieteria"}

        logger.info("Request arguments {}".format(args))
        userdata = self.process_req(args['username'],args['email'],args['contact'])

        if userdata and userdata.count():
            json_resp = self.process_query(userdata)
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp
        return encrypt_resp({"Message":"No record found"})

    def post(self):
        args = self.args
        resp = {}
        if not (args['username'] and args['email'] and args['contact']):
            resp = {"Error": "Required parameters \"username\" \"email\" \"password\" "}
            encrypted_resp = encrypt_resp(resp)
            return encrypted_resp

        userdata = User.query.filter(User.username==args['username'],User.email==args['email'],
                                     User.contact==args['contact'])
        if userdata.count():
            json_resp = self.process_query(userdata)
            json_resp["message"] = "Records Founds against given fields"
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp

        newrecord = User(username=args['username'],email=args['email'],contact=args['contact'])
        newrecord.save()
        userdata = User.query.filter(User.username == args['username'], User.email == args['email'],
                                     User.contact == args['contact'])
        json_resp = self.process_query(userdata)
        json_resp["message"] = "New Record Created"
        encrypted_resp = encrypt_resp(json_resp)
        return encrypted_resp

    def delete(self):
        args = self.args
        if not (args['username'] or args['email'] or args['contact']):
            json_resp = {"Error": "Please provide at least one filteration crieteria"}
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp

        userdata = self.process_req(args['username'], args['email'], args['contact'])
        if userdata and userdata.count():
            json_resp = self.process_query(userdata)
            userdata = self.process_req(args['username'], args['email'], args['contact'])
            for record in userdata:
                record.remove()
            json_resp["message"] = "Given Records are successfully deleted"
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp

        json_resp = {"Message":"No record found"}
        encrypted_resp = encrypt_resp(json_resp)
        return encrypted_resp

    def put(self,username=None,email=None,contact=None):
        args = self.args
        if not (args['username'] or args['email'] or args['contact']):
            json_resp = {"Error": "Please provide at least one filteration crieteria"}
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp
        userdata = self.process_req(args['username'], args['email'], args['contact'])
        count = userdata.count()

        if not count:
            json_resp = {"Message":"No Record found for update"}
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp

        if not (args['username_update'] or args['email_update'] or args['contact_update']):
            json_resp = {"Error": "Please provide at least one update crieteria","Available_record":count}
            encrypted_resp = encrypt_resp(json_resp)
            return encrypted_resp
        try:
            update_resp = self.update_queryset(userdata,args['username_update'], args['email_update'],
                                               args['contact_update'])
        except Exception as e:
            update_resp = {"Error":"Update Failed","ErrorMsg":e}

        encrypted_resp = encrypt_resp(update_resp)
        return encrypted_resp


api.add_resource(Task,'/')

if __name__ == '__main__':
    app.run(debug=True)