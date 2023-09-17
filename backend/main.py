from flask import Flask, jsonify

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import manageApplicants
import manageJobPosting
import manageEmployer
import tools

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from the Python backend!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)



uri = "mongodb+srv://our-first-user:1sJ4VFKtpAss1eEZ@cluster0.za0rs94.mongodb.net/waterloodontwork?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == "__main__":
    db = client.waterloodontwork
    tools.wipe(db)

    applicantA = {
        "name": "John Doe",
        "location": "Waterloo, ON",
        "birthday": "January 1, 2000",
        "skills": ["C/C++", "Python"],
        "education": ["BCS University of Waterloo"],
        "experiences": ["Intern @ Facebook"],
        "projects": ["Cured Cancer"],
        "awards": [],
        "jobList": [],
        "appliedList": []
    }

    companyA = {
        "employer": "Apple",
        "verification": "tim.cook@apple.com",
        "description": "A Small Indie Tech Company",
        "website": "apple.com",
        "socials": ["LinkedIn"],
        "jobs": []
    }

    jobA = {
        "employer": "Apple",
        "position": "SWE Intern Winter 2024",
        "description": "lorem ipsum",
        "skills": ["Swift, C/C++"],
        "qualifications": "lorem ipsum",
        "cutoff": 0,
        "responseTime": 14,
        "applicants": [],
        "candidates": []
    }

    applicantAID = manageApplicants.createApplicant(db, applicantA)
    companyAID = manageEmployer.createEmployer(db, companyA)
    jobAID = manageJobPosting.createJob(db, jobA, companyAID)

    manageApplicants.writeJobList(db, applicantID=applicantAID, jobIDList=[jobAID])
    manageEmployer.addJob(db, employerID=companyAID, jobID=jobAID)

    manageApplicants.applyJob(db, applicantAID, jobAID)
    manageApplicants.withdrawJob(db, applicantAID, jobAID)

    # manageApplicants.deleteApplicant(db, applicantAID)
    # applicantAID = None

    # manageEmployer.removeJob(db, employerID=companyAID, jobID=jobAID)
    # jobAID = None

    manageEmployer.deleteEmployer(db, companyAID)
    companyAID = None

    print("All operations completed. Closing MongoDB.")
    client.close()