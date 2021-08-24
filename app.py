from flask import Flask, json, request
from flask_restful import Api
from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
import jwt
from functools import wraps
from healthdash import healthdash
from auth import auth
from vhosts import vhosts

app = Flask(__name__)
app.register_blueprint(healthdash, url_prefix='/healthdash')
app.register_blueprint(vhosts, url_prefix='/vhosts')
app.register_blueprint(auth, url_prefix='/auth')
api = Api(app)

configfile = open('config.json')
data = json.load(configfile)

app.config['MYSQL_HOST'] = data["API_HOST"]
app.config['MYSQL_USER'] = data["API_USER"]
app.config['MYSQL_PASSWORD'] = data["API_PASS"]
app.config['MYSQL_DB'] = data["API_DB"]
app.config['SECRET_KEY'] = data["SECRET_KEY"]

mysql = MySQL(app)

app.config['MYSQL'] = mysql

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

if __name__ == '__main__':
     app.run(port='5000')