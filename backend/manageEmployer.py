def createEmployer(db, employerData) -> str:
    employers = db.employers
    employerID = employers.insert_one(employerData).inserted_id
    return employerID

def updateEmployer(db, employerID, employerData) -> None:
    employers = db.employers
    employers.replace_one({"_id": employerID}, employerData, upsert=True)

def addJob(db, employerID, jobID) -> None:
    employers = db.employers
    employers.update_one({"_id": employerID}, {"$addToSet": {"jobs": jobID}})

def removeJob(db, employerID, jobID) -> None:
    employers = db.employers
    
    