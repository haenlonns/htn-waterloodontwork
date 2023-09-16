from main import db

def createJob(jobData) -> str:
    jobs = db.jobs
    jobID = jobs.insert_one(jobData).inserted_id
    return jobID

def updateJob(jobID, jobData) -> None:
    


class Job:

    def __init__(self, cutoff=0.8, qualifications: set[str]=set(), responseDays=14) -> None:
        self.cutoff = cutoff
        self.qualifications = qualifications
        self.responseDays = responseDays


