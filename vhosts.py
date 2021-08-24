from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask import Flask, Blueprint, current_app, request

vhosts = Blueprint('vhosts', __name__)

@vhosts.route('/list')
def GetAllVHosts():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vhosts")
    result = cursor.fetchall()
    hosts = []
    
    #json_data=[]
    for data in result:
        hosts.append({
            'id': data[0],
            'name': data[1],
            'datecreated': data[2].strftime("%d-%m-%Y"),
            'active': data[3]
        })

    return jsonify(hosts)

@vhosts.route('/<int:id>')
def GetVHostByID(id):
    hostid = request.headers.get('hostid')
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vhosts WHERE id = " + str(hostid))
    result = cursor.fetchall()
    host = []
    
    #json_data=[]
    for data in result:
        host.append({
            'id': data[0],
            'name': data[1],
            'datecreated': data[2].strftime("%d-%m-%Y"),
            'active': data[3]
        })

    return jsonify(host)

@vhosts.route('/insert')
def InsertVHost():
    hostname = request.headers.get('hostname')
    dateoftoday = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO vhosts (name, datecreated, active) VALUES ('" + hostname + "', '" + dateoftoday + "', 1)")

    return jsonify("OK")

@vhosts.route('/<int:id>/enable')
def EnableVHost():
    hostid = request.headers.get('hostid')
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE vhosts SET active = 1 WHERE id = " + str(hostid))
    return jsonify("OK")

@vhosts.route('/<int:id>/disable')
def DisableVHost():
    hostid = request.headers.get('hostid')
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE vhosts SET active = 0 WHERE id = " + str(hostid))
    return jsonify("OK")

@vhosts.route('/<int:id>/update')
def UpdateVHost(id):
    hostid = request.headers.get('hostid')
    hostname = request.headers.get('hostname')
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE vhosts SET name = '" + hostname + "' WHERE id = " + str(hostid))
    return jsonify("OK")

@vhosts.route('/<int:id>/delete')
def DeleteVHost(id):
    hostid = request.headers.get('hostid')
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM vhosts WHERE id = " + str(hostid))
    return jsonify("OK")