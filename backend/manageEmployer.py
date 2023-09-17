from configure import db
from manageJob import createJob, deleteJob

def createEmployer(employerData) -> str:
    employers = db.employers
    employerID = employers.insert_one(employerData).inserted_id
    return employerID

def deleteEmployer(employerID) -> None:
    employers = db.employers
    employer = employers.find_one({"_id": employerID})
    employerJobs = employer["jobs"]

    for jobID in employerJobs:
        deleteJob(jobID)
    
    employers.delete_one({"_id": employerID})

def getEmployer(employerID):
    employers = db.employers
    return employers.find_one({"_id": employerID})

def addJob(jobData, employerID) -> None:
    employers = db.employers
    jobID = createJob(jobData, employerID)
    employers.update_one({"_id": employerID}, {"$push": {"jobs": jobID}})

    return jobID

def removeJob(employerID, jobID) -> None:
    employers = db.employers
    employers.update_one({"_id": employerID}, {"$pull": {"jobs": jobID}})
    deleteJob(jobID)
    