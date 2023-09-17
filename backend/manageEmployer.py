from manageJobPosting import deleteJob

def createEmployer(db, employerData) -> str:
    employers = db.employers
    employerID = employers.insert_one(employerData).inserted_id
    return employerID

def updateEmployer(db, employerID, employerData) -> None:
    employers = db.employers
    employers.replace_one({"_id": employerID}, employerData, upsert=True)

def deleteEmployer(db, employerID) -> None:
    employers = db.employers
    employer = employers.find_one({"_id": employerID})
    employerJobs = employer["jobs"]

    for jobID in employerJobs:
        deleteJob(db, jobID)
    
    employers.delete_one({"_id": employerID})

def addJob(db, employerID, jobID) -> None:
    employers = db.employers
    employers.update_one({"_id": employerID}, {"$push": {"jobs": jobID}})

def removeJob(db, employerID, jobID) -> None:
    employers = db.employers
    employers.update_one({"_id": employerID}, {"$pull": {"jobs": jobID}})
    deleteJob(db, jobID)

    