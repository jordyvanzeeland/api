from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from functions import token_required
from flask import Flask, Blueprint, current_app

healthdash = Blueprint('healthdash', __name__)

@healthdash.route('/weights')
# @token_required
def HealthDash_Measurements():
    mysql = current_app.config['MYSQL']
    current_length = 173
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_measurements ORDER BY date ASC")
    result = cursor.fetchall()
    weights = []
    
    for data in result:
        bmi = float(data[3]) / (current_length/100)**2
        weights.append({
            'weight': data[3],
            'weight_bmi': str(round(bmi, 1)),
            'weight_date': data[1].strftime("%d-%m-%Y")
        })

    return jsonify(weights)

@healthdash.route('/weights/stats')
# @token_required
def HealthDash_Stats():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_measurements ORDER BY date ASC")
    result = cursor.fetchall()
    stats = []

    cursor2 = mysql.connection.cursor()
    cursor2.execute("SELECT * FROM healthdash_measurements ORDER BY value ASC LIMIT 1")
    result2 = cursor2.fetchone()

    first_item = result[0]
    last_item = (result[len(result) - 1])
    current_length = 173
    bmi = float(last_item[3]) / (current_length/100)**2
    lowest_weight = result2[3]

    stats.append({
        'start_weight': first_item[3],
        'current_weight': last_item[3],
        'weight_loss': str(round((float(first_item[3]) - float(last_item[3])), 1)),
        'current_bmi': str(round(bmi, 1)),
        'lowest_weight': lowest_weight,
        'increase': str(round((float(last_item[3]) - float(lowest_weight)), 1)),
    })

    return jsonify(stats)