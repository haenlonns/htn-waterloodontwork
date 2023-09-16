class Job:

    def __init__(self, cutoff=0.8, qualifications: set[str]=set(), responseDays=14) -> None:
        self.cutoff = cutoff
        self.qualifications = qualifications
        self.responseDays = responseDays


