from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from employers import manageEmployer
import manageApplicants

uri = "mongodb+srv://our-first-user:1sJ4VFKtpAss1eEZ@cluster0.za0rs94.mongodb.net/waterloodontwork?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.waterloodontwork
jobs = db.jobs
employers = db.employers

job = {
    "company": "Apple",
    "position": "SWE Intern Winter 2024",
    "description": "lorem ipsum",
    "qualifications": ["Swift, C/C++, Pursuing Bachelors in CS"],
    "prior internships": 3,
}
job_id = jobs.insert_one(job).inserted_id

employerA = manageEmployer.createEmployer("Apple", "dummy@gmail.com", "Small Indie Tech Company", "apple.com", [], [job_id])
employer_id = employers.insert_one(employerA).inserted_id
employerA = manageEmployer.createEmployer("Tangerine", "dummy@gmail.com", "Small Indie Tech Company", "apple.com", [], [job_id])
employers.replace_one({"_id": employer_id}, employerA)

print(job_id)
print(employer_id)