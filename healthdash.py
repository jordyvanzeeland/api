from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from flask import Flask, Blueprint, current_app

healthdash = Blueprint('healthdash', __name__)

@healthdash.route('/weights')
def HealthDash_Measurements():
    mysql = current_app.config['MYSQL']
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

@healthdash.route('/weights/stats')
def HealthDash_Stats():
    mysql = current_app.config['MYSQL']
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

@healthdash.route('/activities')
def HealthDash_Activities():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM healthdash_activities")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    json_data=[]
    for measurement in result:
        json_data.append(dict(zip(row_headers,measurement)))

    return jsonify(json_data)

@healthdash.route('/bmi')
def HealthDash_BMI():
    current_length = 173
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT value FROM healthdash_measurements WHERE type='weight' ORDER BY healthdash_measurements.date DESC LIMIT 1")
    result = cursor.fetchone()
    bmi = float(result[0]) / (current_length/100)**2

    return jsonify({"bmi" : str(round(bmi, 1))})