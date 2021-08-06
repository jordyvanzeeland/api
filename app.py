from flask import Flask, config, json, request, make_response
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps
import hashlib, binascii, os

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

# Require token for api calls
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            tokendata = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


# Hash a password for storing.
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# Verify a stored password against one provided by user
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# Authentication
@app.route('/login', methods=['POST'])
def login():
    args = request.args
    username = args['username']
    password = args['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from api_users WHERE username = %s", [username])
    result = cursor.fetchone()

    password = verify_password(str(result[3]), str(password))

    if result[2] == username and password == True:
        token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/register', methods=['POST'])
def addUser():
    args = request.args
    name = args['name']
    username = args['username']
    password = args['password']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO api_users (name, username, password) VALUES (%s, %s, %s)", (name, username, hash_password(password)))
    mysql.connection.commit()
    cursor.close()
    return 'OK'

# Get list of all measurements
@app.route('/healthdash/weights', methods=['GET'])
# @token_required
def HealthDash_Measurements():
    current_length = 173
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_measurements where type='weight' ORDER BY healthdash_measurements.date ASC")
    result = cursor.fetchall()
    weights = []
    
    #json_data=[]
    for data in result:
        bmi = float(data[3]) / (current_length/100)**2
        weights.append({
            'weight': data[3],
            'weight_bmi': str(round(bmi, 1)),
            'weight_date': data[1].strftime("%d-%m-%Y")
        })

    return jsonify(weights)

# Get weight stats
@app.route('/healthdash/weights/stats', methods=['GET'])
def HealthDash_Stats():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_measurements where type='weight' ORDER BY healthdash_measurements.date ASC")
    result = cursor.fetchall()
    stats = []

    first_item = result[0]
    last_item = (result[len(result) - 1])
    current_length = 173
    bmi = float(last_item[3]) / (current_length/100)**2

    stats.append({
        'start_weight': first_item[3],
        'current_weight': last_item[3],
        'weight_loss': str(round((float(first_item[3]) - float(last_item[3])), 1)),
        'current_bmi': str(round(bmi, 1))
    })

    return jsonify(stats)

# Get list of all activities
@app.route('/healthdash/activities', methods=['GET'])
# @token_required
def HealthDash_Activities():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_activities")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    json_data=[]
    for measurement in result:
        json_data.append(dict(zip(row_headers,measurement)))
    return jsonify(json_data)


# Get BMI of latest weight added
@app.route('/healthdash/bmi', methods=['GET'])
@token_required
def HealthDash_BMI():
    current_length = 173
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT value FROM healthdash_measurements WHERE type='weight' ORDER BY healthdash_measurements.date DESC LIMIT 1")
    result = cursor.fetchone()
    bmi = float(result[0]) / (current_length/100)**2
    return jsonify({"bmi" : str(round(bmi, 1))})

if __name__ == '__main__':
     app.run(port='5000')