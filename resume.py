from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from functions import token_required
from datetime import datetime
from flask import Flask, Blueprint, current_app, request

resume = Blueprint('resume', __name__)

@resume.route('/personal')
@token_required
def getPersonalData():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM resume_personal")
    result = cursor.fetchall()
    personal = []
    
    for data in result:
        personal.append({
            'param': data[1],
            'value': data[2]
        })

    return jsonify(personal)

@resume.route('/jobs')
@token_required
def getJobsData():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM resume_jobs")
    result = cursor.fetchall()
    jobs = []
    
    for data in result:

        if data[4] != None:
            date_end = data[4].strftime("%m-%Y")
        else:
            date_end = "heden"


        jobs.append({
            'id': data[0],
            'company': data[1],
            'jobtitle': data[2],
            'datestart': data[3].strftime("%m-%Y"),
            'dateend': date_end
        })

    return jsonify(jobs)

@resume.route('/education')
@token_required
def getEducationData():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM resume_education")
    result = cursor.fetchall()
    education = []
    
    for data in result:
        education.append({
            'id': data[0],
            'schoolname': data[1],
            'educationname': data[2],
            'yearstart': data[3].strftime("%Y"),
            'yearend': data[4].strftime("%Y"),
            'diploma': data[5]
        })

    return jsonify(education)

@resume.route('/skills')
@token_required
def getSkillsData():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM resume_skills")
    result = cursor.fetchall()
    skills = []
    
    for data in result:
        skills.append({
            'name': data[0]
        })

    return jsonify(skills)