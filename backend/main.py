from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configure import client

import manageApplicants
import manageJob
import manageEmployer
import manageResponses
import tools

applicant = {
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

company = {
    "employer": "Apple",
    "verification": "tim.cook@apple.com",
    "description": "A Small Indie Tech Company",
    "website": "apple.com",
    "socials": ["LinkedIn"],
    "jobs": []
}

job = {
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

response = {
    "name": "John Doe",
    "skills": ["C/C++"],
    "education": ["BCS University of Waterloo"],
    "experiences": ["Intern @ Facebook"],
    "projects": ["Cured Cancer"],
    "awards": [],
}

tools.wipe()
applicantID = manageApplicants.createApplicant(applicant)
employerID = manageEmployer.createEmployer(company)
jobID = manageEmployer.addJob(job, employerID)
responseID = manageApplicants.applyJob(response, applicantID, jobID)
manageResponses.decideResponse(responseID, "Success")

client.close()
