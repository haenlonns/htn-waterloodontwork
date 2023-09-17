# Should be called as an API from Front-end
def createApplicant(db, applicantData) -> str:
    applicants = db.applicants
    applicantID = applicants.insert_one(applicantData).inserted_id
    applicants.update_one({"_id": applicantID}, {"$set": {"jobList": []}}, upsert=True)
    return applicantID

def updateApplicant(db, applicantID, applicantData) -> None:
    applicants = db.applicants
    applicants.replace_one({"_id": applicantID}, applicantData, upsert=True)

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

def writeJobList(db, applicantID, jobIDList: list[str]) -> None:
    jobs = db.jobs
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

def applyJob(db, applicantID, jobID) -> None:
    applicants = db.applicants
    jobs = db.jobs

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

    applicants.update_one({"_id": applicantID}, {"$pull": {"appliedList": jobID}})
    applicants.update_one({"_id": applicantID}, {"$push": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$pull": {"applicants": applicantID}})
    jobs.update_one({"_id": jobID}, {"$push": {"candidates": applicantID}})
