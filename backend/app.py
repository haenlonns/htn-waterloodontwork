from flask import Flask, jsonify, request
from flask_cors import CORS

import bson

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import manageApplicants
import manageJob
import manageEmployer
import tools

uri = "mongodb+srv://our-first-user:1sJ4VFKtpAss1eEZ@cluster0.za0rs94.mongodb.net/waterloodontwork?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.waterloodontwork

app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def close_mongodb_connection(exception=None):
    client.close()

@app.route("/api/postApplicant", methods=["POST", "GET"])
def getApplicantData():
    bsonData = request.data
    applicantData = bson.loads(bsonData)
    applicantID = manageApplicants.createApplicant(db, applicantData)
    manageApplicants.writeJobList(db, applicantID)
    return jsonify(applicantID)

@app.route("/api/postEmployer", methods=["POST", "GET"])
def getEmployerData():
    bsonData = request.data
    employerData = bson.loads(bsonData)
    employerID = manageEmployer.createEmployer(db, employerData)
    return jsonify(employerID)

@app.route("/api/postJob", methods=["POST", "GET"])
def getJobData():
    bsonData = request.data
    designaledData = bson.loads(bsonData)
    jobData = designaledData["jobData"]
    employerID = designaledData["employerID"]
    jobID = manageEmployer.addJob(db, jobData, employerID)
    return jsonify(jobID)

if __name__ == '__main__':
    app.run(debug=True)