from flask import Flask, jsonify, request
from flask_cors import CORS

import bson

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import manageApplicants
import manageJob
import manageEmployer
import manageResponses
import tools

uri = "mongodb+srv://our-first-user:1sJ4VFKtpAss1eEZ@cluster0.za0rs94.mongodb.net/waterloodontwork?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.waterloodontwork

app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def close_mongodb_connection(exception=None):
    client.close()



@app.route("/applicant/postApplicant", methods=["POST", "GET"])
def getApplicantData():
    bsonData = request.data
    applicantData = bson.loads(bsonData)
    applicantID = manageApplicants.createApplicant(db, applicantData)
    manageApplicants.writeJobList(db, applicantID)
    return applicantID

@app.route("/applicant/getJob", methods=["GET"])
def postJobData():
    jobID = request.data.decode('utf-8')
    jobData = manageJob.getJob(db, jobID)
    return jsonify(jobData)

@app.route("/applicant/applyJob", methods=["POST"])
def applyJob():
    bsonData = request.data
    designaledData = bson.loads(bsonData)
    responseData = designaledData["responseData"]
    applicantID = designaledData["applicantID"]
    jobID = designaledData["jobID"]
    manageApplicants.applyJob(db, responseData, applicantID, jobID)
    return applicantID



@app.route("/employer/postEmployer", methods=["POST"])
def getEmployerData():
    bsonData = request.data
    employerData = bson.loads(bsonData)
    employerID = manageEmployer.createEmployer(db, employerData)
    return employerID

@app.route("/employer/postJob", methods=["POST"])
def getJobData():
    bsonData = request.data
    designaledData = bson.loads(bsonData)
    jobData = designaledData["jobData"]
    employerID = designaledData["employerID"]
    jobID = manageEmployer.addJob(db, jobData, employerID)
    return jobID

@app.route("/employer/getResponse", methods=["GET"])]
def postResponseData():
    responseID = request.data.decode('utf-8')
    responseData = manageResponses.getResponse(db, responseID)
    return jsonify(responseData)

if __name__ == '__main__':
    app.run(debug=True)