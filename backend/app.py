from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config
from configure import client
import bson

import manageApplicants
import manageJob
import manageEmployer
import manageResponses
import tools

app = Flask(__name__)
CORS(app)

db = client.waterloodontwork

@app.teardown_appcontext
def close_mongodb_connection(exception=None):
    client.close()


@app.route("/applicant/postApplicant", methods=["POST"])
def getApplicantData():
    bsonData = request.data
    applicantData = bson.loads(bsonData)
    applicantID = manageApplicants.createApplicant(applicantData)
    manageApplicants.writeJobList(applicantID)
    return applicantID

@app.route("/applicant/getJob", methods=["GET"])
def postJobData():
    jobID = request.data.decode('utf-8')
    jobData = manageJob.getJob(jobID)
    return jsonify(jobData)

@app.route("/applicant/applyJob", methods=["POST"])
def applyJob():
    bsonData = request.data
    designaledData = bson.loads(bsonData)
    responseData = designaledData["responseData"]
    applicantID = designaledData["applicantID"]
    jobID = designaledData["jobID"]
    responseID = manageApplicants.applyJob(responseData, applicantID, jobID)
    return responseID


@app.route("/employer/postEmployer", methods=["POST"])
def getEmployerData():
    bsonData = request.data
    employerData = bson.loads(bsonData)
    employerID = manageEmployer.createEmployer(employerData)
    return employerID

@app.route("/employer/postJob", methods=["POST"])
def getJobData():
    bsonData = request.data
    designaledData = bson.loads(bsonData)
    jobData = designaledData["jobData"]
    employerID = designaledData["employerID"]
    jobID = manageEmployer.addJob(jobData, employerID)
    return jobID

@app.route("/employer/postDecision", methods=["POST"])
def getDecisionData():
    bsonData = request.data
    designaledData = bson.loads(bsonData)

    responseID = designaledData["responseID"]
    decision = designaledData["decision"]

    manageResponses.decideResponse(responseID, decision)


@app.route("/general/getResponse", methods=["GET"])
def postResponseData():
    responseID = request.data.decode('utf-8')
    responseData = manageResponses.getResponse(responseID)
    return jsonify(responseData)


if __name__ == '__main__':
    app.run(debug=True)
