from main import db

# Should be called as an API from Front-end
def createApplicant(applicantData) -> str:
    applicants = db.applicants
    applicantID = applicants.insert_one(applicantData).inserted_id
    applicants.update_one({"_id": applicantID}, {"$set": {"jobList": []}}, upsert=True)
    return applicantID

def updateApplicant(applicantID, applicantData) -> None:
    applicants = db.applicants
    applicant = applicants.replace_one({"_id": applicantID}, applicantData, upsert=True)

def writeJobList(applicantID, jobIDList: list[str]) -> None:
    jobs = db.jobs
    applicants = db.applicants
    applicantJobList = set()

    for jobID in jobIDList:
        job = jobs.find_one({"_id": jobID})
        applicant = applicants.find_one({"_id": applicantID})

        relevantSkills = set.intersection(set(job.qualifications), set(applicant.qualifications))
        compatabilityIndex = len(relevantSkills) / len(job.qualifications)

        if compatabilityIndex >= job.cutoff:
            applicantJobList.add(jobID)
    
    applicants.update_one({"_id": applicantID}, {"$set": {"jobList": applicantJobList}}, upsert=True)
