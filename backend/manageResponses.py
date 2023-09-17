def createResponse(db, responseData, applicantID, jobID) -> str:
    responses = db.responses
    jobs = db.jobs

    responseID = responses.insert_one(responseData).inserted_id

    responses.update_one({"_id": responseID}, {"$set": {"applicantID": applicantID}})
    responses.update_one({"_id": responseID}, {"$set": {"jobID": jobID}})

    jobs.update_one({"_id": jobID}, {"$push": {"responses": responseID}})

    return responseID

def deleteResponse(db, responseID) -> None:
    responses = db.responses
    applicants = db.applicants
    jobs = db.jobs

    response = responses.find_one({"_id": responseID})

    applicantID = response["applicantID"]
    jobID = response["jobID"]

    applicants.update({"_id": applicantID}, {"$pull": {"responses": responseID}})
    jobs.update_one({"_id": jobID}, {"$pull": {"responses": responseID}})

    responses.delete_one({"_id": responseID})

def getResponse(db, responseID):
    responses = db.responses
    return responses.find_one({"_id": responseID})
