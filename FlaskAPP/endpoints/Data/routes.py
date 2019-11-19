import os
from io import BytesIO
from FlaskAPP.config import Config
import json
from FlaskAPP import ma, db
from sqlalchemy import desc, asc
from sqlalchemy.sql.expression import func
from flask import Flask, Blueprint, Response, render_template, redirect, url_for, request, jsonify, send_file
from FlaskAPP.models.questions import Questions
from FlaskAPP.models.jsonfiles import JSONFiles
from FlaskAPP.models.circles import Circles
from FlaskAPP.models.answers import Answers
from FlaskAPP.models.pressure import Pressure
from FlaskAPP.models.testframe import TestFrame
from FlaskAPP.models.doctor import Doctor
from random import randint
import flask_marshmallow
import xlsxwriter
import datetime, time
from .Util import circle_fill, pressure_fill

app = Flask(__name__)

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Questions


class JSONFileSchema(ma.ModelSchema):
    class Meta:
        model = JSONFiles

class DoctorFileSchema(ma.ModelSchema):
    class Meta:
        model = Doctor


data = Blueprint('data', __name__)

# Divdies to get milliseconds, then subtracts from the start time to get interval
@data.route("/data/upload_patient_test_data", methods=['POST'])
def upload_patient_test_data():
    try:
        testData = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    
    # Get testframe data
    testID = round(time.time())
    doctorID = testData["doctorID"]
    patientID = testData["patientID"]
    testStartTime = testData["testStartTime"] 
    testEndTime = testData["testEndTime"]
    testName = testData["testName"]

    if testName is None:
        testName = "AlphabetTest.json"

    if(testName == "AlphabetTest"):
        testName = "AlphabetTest.json"

    # Get the difference in time from start to end, then convert to seconds
    length = testEndTime - testStartTime
    testLength = datetime.timedelta(seconds=length)

    # Target symbol to circle
    targetSymbol = testData["answerSymbol"]

    # Begin transaction
    db.session.rollback()

    # Create the row for the test frame
    testframe = TestFrame(TestID = testID, PatientID = patientID, 
        DoctorID = doctorID, DateTaken = str(datetime.date.today()), 
        TestName = testName, TestLength = testLength)

    db.session.add(testframe)
    db.session.commit()

    db.session.rollback()
    # Loop through each circle made
    for i in range(len(testData["patientAnswers"])):
        
        currentSymbol = testData["patientAnswers"][i]
        currentTouchDataArray = testData["patientAnswerTouchData"][i]

        # Get intervals 
        beginTime = currentTouchDataArray[0]['time']
        endTime = currentTouchDataArray[len(currentTouchDataArray)-1]['time']
        totalTime = endTime - beginTime

        # Create a row for circle, then add it
        CircleRow = Circles(TestID = testID, CircleID = i+1, 
                symbol = currentSymbol['name'], begin_circle = beginTime,
                end_circle = endTime, total_time = totalTime)

        db.session.add(CircleRow)

    db.session.commit()
    db.session.rollback()

    # Loop through the pressure data
    # Important this is committed separately to avoid foreign key constraints
    for i in range(len(testData["patientAnswers"])):
        
        currentSymbol = testData["patientAnswers"][i]
        currentTouchDataArray = testData["patientAnswerTouchData"][i]    
        
        # Loop through Touch Data, PressureIDCounter counts each touch made, per circle
        PressureIDCounter = 1
        for point in currentTouchDataArray:
                
                # you have access to each point in the touch array
                PressureRow = Pressure(TestID = testID, CircleID = i+1, PressureID = PressureIDCounter,
                    Xcoord = point['x'], Ycoord = point['y'], Pressure = point['force'], 
                    Azimuth= point['azimuthAngle'], PenAltitude = point['altitudeAngle'])
                PressureIDCounter += 1
                db.session.add(PressureRow)

    # Complete transaction
    db.session.commit()
    db.session.close()

    return "Nice!"

@data.route("/data/testConnection")
def testConnection():
    return "Good job!"


@data.route("/data/upload_patient_questionnaire_answers", methods=['POST'])
def upload_patient_questionnaire_answers():
    try:
        data = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    
    db.session.rollback()

    testframe = TestFrame.query.order_by(desc(TestFrame.TestID)).first()

    testID = testframe.TestID

    for question in data["answers"]:
        answer = question["Answer"]
        questionID = question["QuestionID"]

        # Add row for each answer given
        row = Answers(TestID = testID, QuestionID = questionID, Answer = answer)
        db.session.add(row)

    db.session.commit()

    return "Answers"

@data.route('/data/download/<filename>')
def download(filename):
    file_data = JSONFiles.query.filter_by(name=filename).first()
    jsonfile = file_data.data

    file = jsonfile.decode("utf8")

    return file

@data.route('/data/download/getTestList')
def getList():
    fileList = JSONFiles.query.all()
    file_schema = JSONFileSchema(many=True, only=['name'])
    output = file_schema.dump(fileList)
    return jsonify(output)
# make sure to perform error checking - this endpoint is open to anyone

@data.route('/data/download/getDoctorList')
def getDoctorList():
    doctorList = Doctor.query.all()
    doctor_schema = DoctorFileSchema(many=True, only=['DoctorID', 'DoctorName'])
    output = doctor_schema.dump(doctorList)
    return jsonify(output)

@data.route("/data/download_questions", methods=['GET'])
def download_questions():

    questions = Questions.query.order_by(Questions.QuestionID).all()
    question_schema = QuestionSchema(many=True)
    output = question_schema.dump(questions)
    return jsonify(output)

#  ENDPOINT
#  returns corresponding .xlsx file based on get request header
#  <TestID> := ID of the test selected
#  <selection> := Either Data or Questionnaire
#  ***Will need to implement a garbage collector for /file-downloads folder after X (hours/day)***


@data.route('/data/get_test_data_excel', methods=['GET'])
def get_test_data_excel():
    test_id = request.args.get('id', None)
    selection = request.args.get('selection', None)
    testinfo = TestFrame.query.filter_by(TestID=test_id).first()  # get test info

    row = 1
    col = 0

    dir_path = Config.APP_ROOT + '/file-downloads/'
    filename = "{id}_testdata".format(id=testinfo.PatientID) + str(round(time.time())) + ".xlsx"

    workbook = xlsxwriter.Workbook(dir_path + filename)  # Create xlsx file
    #  formula = workbook.add_worksheet('formula')
    raw_circle = workbook.add_worksheet('circle')
    raw_pressure = workbook.add_worksheet('pressure')
    final = workbook.add_worksheet('formula')

    # Grab all points from table
    circles = db.engine.execute("SELECT * FROM test.circles WHERE TestID='{id}';".format(id=test_id))
    pressure = Pressure.query.filter_by(TestID=test_id).all()  # get pressure from test

    circle_fill(raw_circle, testinfo, circles)  # generate circle file

    pressure_fill(raw_pressure, pressure)  # generate pressure file

    workbook.close()
    return send_file(dir_path + filename, as_attachment=True)  # send file as attachment

@data.route('/data/get_questionnaire_excel')
def get_questionnaire_excel():
        test_id = request.args.get('id', None)
        selection = request.args.get('selection', None)
        testinfo = TestFrame.query.filter_by(TestID=test_id).first()  # get test info

        # @TODO: move to Util.py file
        dir_path = Config.APP_ROOT + '/file-downloads/'
        filename = "{id}_questionnaire".format(id=testinfo.PatientID) + str(round(time.time())) + ".xlsx"

        excel = xlsxwriter.Workbook(dir_path + filename)
        question = excel.add_worksheet()
        question.set_column(0, 1, 25)
        question.set_column(2, 3, 75)
        question.set_column(4, 4, 50)
        question.write(0, 0, 'QuestionID')
        question.write(0, 1, 'QuestionType')
        question.write(0, 2, 'PossibleAnswers')
        question.write(0, 3, 'Question')
        question.write(0, 4, 'Answer')
        questions = Questions.query.order_by(asc(Questions.QuestionID)).all()
        answers = Answers.query.filter_by(TestID=test_id).order_by(asc(Answers.QuestionID)).all()

        for i in range(0, len(questions)):  # loop questions 3 columns
            question.write(i+1, 0, questions[i].QuestionID)
            question.write(i+1, 1, questions[i].QuestionType)
            question.write(i+1, 2, questions[i].PossibleAnswers)
            question.write(i+1, 3, questions[i].Question)
        
        for answer in answers:
            question.write(answer.QuestionID, 4, answer.Answer)

        excel.close()
        return send_file(dir_path + filename, as_attachment=True)  # send file as attachment
