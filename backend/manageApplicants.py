import manageResponses

def createApplicant(db, applicantData) -> str:
    applicants = db.applicants
    applicantID = applicants.insert_one(applicantData).inserted_id
    applicants.update_one({"_id": applicantID}, {"$set": {"jobList": []}}, upsert=True)
    return applicantID

def deleteApplicant(db, applicantID) -> None:
    applicants = db.applicants
    applicant = applicants.find_one({"_id": applicantID})

    applicantAppliedList = applicant["appliedList"]
    for jobID in applicantAppliedList:
        withdrawJob(db, applicantID, jobID)
    
    applicantJobList = applicant["jobList"]
    for jobID in applicantJobList:
        rejectJob(db, applicantID, jobID)

    applicants.delete_one({"_id": applicantID})

def getApplicant(db, applicantID):
    applicants = db.applicants
    return applicants.find_one({"_id": applicantID})

def writeJobList(db, applicantID) -> None:
    jobs = db.jobs
    aggregateList = list(jobs.aggregate([{"$project": {"_id": 1}}]))
    jobIDList = [job["_id"] for job in aggregateList]
    applicants = db.applicants
    applicant = applicants.find_one({"_id": applicantID})
    applicantJobList = []

    for jobID in jobIDList:
        job = jobs.find_one({"_id": jobID})

        jobSkills = set(job["skills"])
        applicantSkills = set(applicant["skills"])

        relevantSkills = set.intersection(jobSkills, applicantSkills)
        compatabilityIndex = len(relevantSkills) / len(jobSkills)

        if compatabilityIndex >= job["cutoff"]:
            applicantJobList.append(jobID)
            jobs.update_one({"_id": jobID}, {"$push": {"candidates": applicantID}})
    
    applicants.update_one({"_id": applicantID}, {"$set": {"jobList": applicantJobList}})

def applyJob(db, responseData, applicantID, jobID) -> None:
    applicants = db.applicants
    jobs = db.jobs

    responseID = manageResponses.createResponse(db, responseData, applicantID, jobID)
    applicants.update_one({"_id": applicantID}, {"$push": {"responseList": responseID}})

    applicants.update_one({"_id": applicantID}, {"$push": {"appliedList": jobID}})
    applicants.update_one({"_id": applicantID}, {"$pull": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$push": {"applicants": applicantID}})
    jobs.update_one({"_id": jobID}, {"$pull": {"candidates": applicantID}})

def rejectJob(db, applicantID, jobID) -> None:
    applicants = db.applicants
    jobs = db.jobs

    applicants.update_one({"_id": applicantID}, {"$pull": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$pull": {"candidates": applicantID}})

def withdrawJob(db, applicantID, jobID) -> None:
    applicants = db.applicants
    jobs = db.jobs

    job = jobs.find_one({"_id": jobID})
    responseIDSet = job["responses"]

    applicant = applicants.find_one({"_id": applicantID})
    applicantResponseIDSet = applicant["responseList"]

    applicants.update_one({"_id": applicantID}, {"$pull": {"appliedList": jobID}})
    applicants.update_one({"_id": applicantID}, {"$push": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$pull": {"applicants": applicantID}})
    jobs.update_one({"_id": jobID}, {"$push": {"candidates": applicantID}})
