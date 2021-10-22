from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from flask import Flask, Blueprint, current_app
from functions import token_required

projects = Blueprint('projects', __name__)

@projects.route('/get')
@token_required
def getAllProjects():
    mysql = current_app.config['MYSQL']   
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM JMS_projects")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()

    json_data=[]
    for data in result:
        json_data.append(dict(zip(row_headers,data)))

    return jsonify(json_data)

@projects.route('/get/<int:id>')
@token_required
def getProject(id):
    mysql = current_app.config['MYSQL']   
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM JMS_projects WHERE id = %s", (str(id)))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()

    json_data = dict(zip(row_headers,result))

    return jsonify(json_data)