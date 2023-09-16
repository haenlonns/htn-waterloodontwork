'''
Takes in two sets: qualifications and skills
Returns a list of skills in qualifications aka intersection of 
'''

def intersectSkillsets(qualifiactions: set[str], skills: set[str]) -> set[str]:
    return set.intersection(qualifiactions, skills)