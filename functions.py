from flask import Flask, json, request, current_app
from flask_jsonpify import jsonify
import jwt
from functools import wraps

# Require token for api calls
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            tokendata = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated