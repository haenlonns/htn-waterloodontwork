def createJob(db, jobData, employerID) -> str:
    jobs = db.jobs
    jobID = jobs.insert_one(jobData).inserted_id
    jobs.update_one({"_id": jobID}, {"$set": {"employerID": employerID}})
    return jobID

def updateJob(db, jobID, jobData) -> None:
    jobs = db.jobs
    jobs.replace_one({"_id": jobID}, jobData, upsert=True)
