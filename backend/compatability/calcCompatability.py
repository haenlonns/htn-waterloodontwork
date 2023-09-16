'''
Returns a float between 0-100 of how compatible a skillset is to a job posting
'''
def calcCompatability(qualifiactions: set[str], intersectSkills: set[str]) -> float:
    return len(intersectSkills) / len(qualifiactions)