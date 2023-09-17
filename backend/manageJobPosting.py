def createJob(db, jobData, employerID) -> str:
    jobs = db.jobs
    jobID = jobs.insert_one(jobData).inserted_id
    jobs.update_one({"_id": jobID}, {"$set": {"employerID": employerID}})
    return jobID

def updateJob(db, jobID, jobData) -> None:
    jobs = db.jobs
    jobs.replace_one({"_id": jobID}, jobData, upsert=True)

def deleteJob(db, jobID) -> None:
    jobs = db.jobs
    job = jobs.find_one({"_id": jobID})
    applicants = db.applicants

    candidateList = job["candidates"]
    applicantList = job["applicants"]

    for applicantID in candidateList:
        applicants.update_one({"_id": applicantID}, {"$pull": {"jobList": jobID}})
    
    for applicantID in applicantList:
        applicants.update_one({"_id": applicantID}, {"$pull": {"appliedList": jobID}})

    jobs.delete_one({"_id": jobID})
