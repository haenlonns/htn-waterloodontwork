# jobs should reference ID
def createEmployer(name: str, verEmail: str, description: str, website: str, socials, jobs: set[str]):
  employer = {
            "employer": name,
            "verification": verEmail,
            "description": description,
            "website": website,
            "socials": socials,
            "jobs": jobs
        }
  

  
  return employer



