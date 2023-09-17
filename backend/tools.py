def wipe(db):
    db.jobs.delete_many({})
    db.applicants.delete_many({})
    db.employers.delete_many({})
