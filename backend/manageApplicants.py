from configure import db
import manageResponses

def createApplicant(applicantData) -> str:
    applicants = db.applicants
    applicantID = applicants.insert_one(applicantData).inserted_id
    applicants.update_one({"_id": applicantID}, {"$set": {"jobList": []}}, upsert=True)
    return applicantID

def deleteApplicant(applicantID) -> None:
    applicants = db.applicants
    applicant = applicants.find_one({"_id": applicantID})

    applicantAppliedList = applicant["appliedList"]
    for jobID in applicantAppliedList:
        withdrawJob(applicantID, jobID)
    
    applicantJobList = applicant["jobList"]
    for jobID in applicantJobList:
        rejectJob(applicantID, jobID)

    applicants.delete_one({"_id": applicantID})

def getApplicant(applicantID):
    applicants = db.applicants
    return applicants.find_one({"_id": applicantID})

def writeJobList(applicantID) -> None:
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

def applyJob(responseData, applicantID, jobID) -> str:
    applicants = db.applicants
    jobs = db.jobs

    responseID = manageResponses.createResponse(responseData, applicantID, jobID)
    applicants.update_one({"_id": applicantID}, {"$push": {"responseList": responseID}})

    applicants.update_one({"_id": applicantID}, {"$push": {"appliedList": jobID}})
    applicants.update_one({"_id": applicantID}, {"$pull": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$push": {"applicants": applicantID}})
    jobs.update_one({"_id": jobID}, {"$pull": {"candidates": applicantID}})

    return responseID

def rejectJob(applicantID, jobID) -> None:
    applicants = db.applicants
    jobs = db.jobs

    applicants.update_one({"_id": applicantID}, {"$pull": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$pull": {"candidates": applicantID}})

def withdrawJob(applicantID, jobID) -> None:
    applicants = db.applicants
    jobs = db.jobs

    job = jobs.find_one({"_id": jobID})
    responseIDSet = set(job["responses"])

    applicant = applicants.find_one({"_id": applicantID})
    applicantResponseIDSet = set(applicant["responseList"])

    responseID = set.intersection(responseIDSet, applicantResponseIDSet).pop()
    manageResponses.deleteResponse(responseID)

    applicants.update_one({"_id": applicantID}, {"$pull": {"appliedList": jobID}})
    applicants.update_one({"_id": applicantID}, {"$push": {"jobList": jobID}})

    jobs.update_one({"_id": jobID}, {"$pull": {"applicants": applicantID}})
    jobs.update_one({"_id": jobID}, {"$push": {"candidates": applicantID}})
