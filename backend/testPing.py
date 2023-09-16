from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from employers import manageEmployer

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://our-first-user:1sJ4VFKtpAss1eEZ@cluster0.za0rs94.mongodb.net/waterloodontwork?retryWrites=true&w=majority"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
                        
# Send a ping to confirm a successful connection
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

employerA = manageEmployer.createEmployer("Apple", "dummy@gmail.com", "Small Indie Tech Company", "apple.com", [], {"Intern": job_id})
employer_id = employers.insert_one(employerA).inserted_id

print(job_id)
print(employer_id)