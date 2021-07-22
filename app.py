from flask import Flask, config, json, request, make_response
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
api = Api(app)

configfile = open('config.json')
data = json.load(configfile)

app.config['MYSQL_HOST'] = data["API_HOST"]
app.config['MYSQL_USER'] = data["API_USER"]
app.config['MYSQL_PASSWORD'] = data["API_PASS"]
app.config['MYSQL_DB'] = data["API_DB"]
app.config['SECRET_KEY'] = data["SECRET_KEY"]

mysql = MySQL(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    args = request.args
    username = args['username']
    password = args['password']

    if username == 'jordy' and password == 'password':
        token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/healthdash/measurements', methods=['GET'])
@token_required
def HealthDash_Measurements():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_measurements")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    json_data=[]
    for measurement in result:
        json_data.append(dict(zip(row_headers,measurement)))
        
    return jsonify(json_data)

@app.route('/healthdash/activities', methods=['GET'])
@token_required
def HealthDash_Activities(self):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_activities")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    json_data=[]
    for measurement in result:
        json_data.append(dict(zip(row_headers,measurement)))
    return jsonify(json_data)


if __name__ == '__main__':
     app.run(port='5000')