from flask import Flask, json, request
from flask_restful import Api
from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from healthdash import healthdash
from auth import auth
from resume import resume
from projects import projects

app = Flask(__name__)
app.register_blueprint(healthdash, url_prefix='/healthdash')
app.register_blueprint(resume, url_prefix='/resume', name="me")
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(projects, url_prefix='/projects')
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

if __name__ == '__main__':
     app.run(port='5000')