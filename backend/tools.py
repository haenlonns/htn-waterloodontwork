from configure import db

def wipe():
    db.jobs.delete_many({})
    db.applicants.delete_many({})
    db.employers.delete_many({})
    db.responses.delete_many({})
