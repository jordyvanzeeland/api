from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from functools import wraps
import jwt
import datetime
import hashlib, binascii, os
from flask import Flask, Blueprint, current_app, request, make_response

auth = Blueprint('auth', __name__)

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

@auth.route('/login', methods=['POST'])
def login():
    args = request.args
    username = args['username']
    password = args['password']

    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from api_users WHERE username = %s", [username])
    result = cursor.fetchone()

    password = verify_password(str(result[3]), str(password))

    if result[2] == username and password == True:
        token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, current_app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@auth.route('/register', methods=['POST'])
def addUser():
    args = request.args
    name = args['name']
    username = args['username']
    password = args['password']

    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO api_users (name, username, password) VALUES (%s, %s, %s)", (name, username, hash_password(password)))
    mysql.connection.commit()
    cursor.close()
    return 'OK'