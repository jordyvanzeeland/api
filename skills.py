from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from functions import token_required
from flask import request, Blueprint, current_app

skills = Blueprint('skills', __name__)

@skills.route('/')
# @token_required
def Skills_list():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT s.id, s.name, s.type as typeid, st.name as type FROM skills s LEFT OUTER JOIN skills_types st ON s.type = st.id")
    result = cursor.fetchall()
    skills = []
    
    for data in result:
        skills.append({
            'id': data[0],
            'name': data[1],
            'typeid': data[2],
            'type': data[3]
        })

    return jsonify(skills)

@skills.route('/types')
# @token_required
def Skills_types():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM skills_types")
    result = cursor.fetchall()
    types = []
    
    for data in result:
        types.append({
            'id': data[0],
            'name': data[1]
        })

    return jsonify(types)

@skills.route('/insert', methods=['POST'])
def addSkill():
    name = request.headers['name']
    type = request.headers['type']

    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO skills (name, type) VALUES (%s, %s)", (name, type))
    mysql.connection.commit()
    cursor.close()
    return 'OK'

@skills.route('/delete', methods=['DELETE'])
def deleteSkill():
    skillid = request.headers['skillid']

    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM skills WHERE id = " + skillid)
    mysql.connection.commit()
    cursor.close()
    return 'OK'