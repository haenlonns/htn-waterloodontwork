from compatability import calcCompatability
from compatability import intersectSkillsets
from jobPostings import jobClass

applicant_template = {
    "name",
    
}

class Applicant:

    # ideally want a mongodb entry to store user skills
    def __init__(self, applicant) -> None:
        self.skillset = applicant()
        self.jobList = []

    def resetJobList(self) -> None:
        del self.jobList[:]
    
    def generateJobList(self, masterList: list[jobClass.Job]) -> None:
        self.resetJobList()
        for job in masterList:
            overlap: set[str] = intersectSkillsets(job.qualifications, self.skillset)
            compatabilityIndex: float = calcCompatability(job.qualifications, overlap)
            if compatabilityIndex >= job.cutoff:
                self.jobList.append(job)

    
    
