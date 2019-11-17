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
def convert(nano, testStartTime):
    return (nano - testStartTime) / 1000000


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
    convertToSeconds = (testEndTime - testStartTime) / 100000000
    testLength = str(datetime.timedelta(seconds=convertToSeconds))

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
        beginTime = convert(currentTouchDataArray[0]['time'], testStartTime)
        endTime = convert(currentTouchDataArray[len(currentTouchDataArray)-1]['time'], testStartTime)
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
                    Xcoord = point['x'], Ycoord = point['y'], Pressure = point['force'])
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


@data.route('/data/get_excel', methods=['GET'])
def get_excel():
    test_id = request.args.get('id', None)
    selection = request.args.get('selection', None)
    testinfo = TestFrame.query.filter_by(TestID=test_id).first()  # get test info

    row = 1
    col = 0

    if selection == '1':  # User requested download for DATA
        dir_path = Config.APP_ROOT + '/file-downloads/'
        filename = "{id}_testdata.xlsx".format(id=testinfo.PatientID)
        if os.path.isfile(dir_path + filename):  # check to see if file already exists
            return send_file(dir_path + filename, as_attachment=True)

        workbook = xlsxwriter.Workbook(dir_path + filename)  # Create xlsx file
        formula = workbook.add_worksheet()
        raw = workbook.add_worksheet()
        final = workbook.add_worksheet()

        # Header
        raw.write(0, 0, 'CircleID')
        raw.write(0, 1, 'symbol')
        raw.write(0, 2, 'begin_circle')
        raw.write(0, 3, 'end_circle')
        raw.write(0, 4, 'total_time')
        raw.write(0, 5, 'CircleID')
        raw.write(0, 6, 'PressureID')
        raw.write(0, 7, 'Pressure')
        raw.write(3, 10, 'PatientID:')
        raw.write(4, 10, testinfo.PatientID)

        # Grab all points from table
        circles = db.engine.execute("SELECT * FROM test.circles WHERE TestID='{id}';".format(id=test_id))
        pressure = Pressure.query.filter_by(TestID=test_id).all()  # get pressure from test
        for item in circles:  # loop circles 5 columns
            raw.write(row, col, item.CircleID)
            raw.write(row, col + 1, item.symbol)
            raw.write(row, col + 2, item.begin_circle)
            raw.write(row, col + 3, item.end_circle)
            raw.write(row, col + 4, item.total_time)
            row = row + 1

        row = 1
        col = 5
        for item in pressure:  # loop pressure 3 columns
            raw.write(row, col, item.CircleID)
            raw.write(row, col + 1, item.PressureID)
            raw.write(row, col + 2, item.Pressure)
            row = row + 1

        workbook.close()
        return send_file(dir_path + filename, as_attachment=True)  # send file as attachment
    elif selection == '2':
        dir_path = Config.APP_ROOT + '/file-downloads/'
        filename = "{id}_questionnaire.xlsx".format(id=testinfo.PatientID)
        if os.path.isfile(dir_path + filename):
            return send_file(dir_path + filename, as_attachment=True)  # send file as attachment

        excel = xlsxwriter.Workbook(dir_path + filename)
        question = excel.add_worksheet()
        question.write(0, 0, 'QuestionID')
        question.write(0, 1, 'QuestionType')
        question.write(0, 2, 'PossibleAnswers')
        question.write(0, 3, 'Question')
        question.write(0, 4, 'Answer')
        questions = Questions.query.order_by(asc(Questions.QuestionID)).all()
        answers = Answers.query.filter_by(TestID=test_id).order_by(asc(Answers.QuestionID)).all()

        for item in questions:  # loop questions 3 columns
            question.write(row, col + 1, item.QuestionID)
            question.write(row, col + 2, item.QuestionType)
            question.write(row, col + 3, item.PossibleAnswers)
            question.write(row, col + 4, item.Question)
            row = row + 1

        row = 1
        col = 5
        for item in answers:  # loop answers 5 columns
            question.write(row, col, item.Answer)
            # questions.write(row, col + 1, item['Answer'])
            row = row + 1

        excel.close()
        return send_file(dir_path + filename, as_attachment=True)  # send file as attachment


