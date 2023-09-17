from manageJob import createJob, deleteJob

def createEmployer(db, employerData) -> str:
    employers = db.employers
    employerID = employers.insert_one(employerData).inserted_id
    return employerID

def deleteEmployer(db, employerID) -> None:
    employers = db.employers
    employer = employers.find_one({"_id": employerID})
    employerJobs = employer["jobs"]

    for jobID in employerJobs:
        deleteJob(db, jobID)
    
    employers.delete_one({"_id": employerID})

def getEmployer(db, employerID):
    employers = db.employers
    return employers.find_one({"_id": employerID})

def addJob(db, jobData, employerID) -> None:
    employers = db.employers
    jobID = createJob(db, jobData, employerID)
    employers.update_one({"_id": employerID}, {"$push": {"jobs": jobID}})

    return jobID

def removeJob(db, employerID, jobID) -> None:
    employers = db.employers
    employers.update_one({"_id": employerID}, {"$pull": {"jobs": jobID}})
    deleteJob(db, jobID)
    