"""
Master data service: this service will be responsible for the metadata for the simulations and manage
at least two data tables in a persistent data store:
•jobs: a table containing metadata information for each submitted simulation job (user who sent
the job, timestamp submitted, status (submitted, processing, done), date range, assets (a collection
of integers from 1 until 100))
•results: a table containing metadata information for the result of each job (job ID, timestamp,
assets/weights (a collection of pairs asset number/a real number between 0.0 and 1.0))
The service will expose an API for submitting jobs and fetching and updating data on running or done
jobs. Note that only users of the user group managers and administrators are allowed to use this service.
All other users and unauthenticated users will get an authorization error
"""


from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import uuid
from datetime import datetime
from users import db
from schemas import Job, Result
from auth import AuthHandler

app = FastAPI()
security = HTTPBearer()
authHandler = AuthHandler()

allowed_roles = ["1", "3"]


    
def check_if_file_exists(filename:str) -> bool:
    try:
        with open(filename, "r") as f:
            return True
    except FileNotFoundError:
        return False

def get_data_from_file(filename:str) -> list:
    if check_if_file_exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        return []
    
def write_data_to_file(filename:str, data:list) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)
        
def get_role(username:str) -> str:
    for user in db:
        if user.username == username:
            return user.role
        
@app.post("/master/job/")
async def create_job(token:str, job:Job):
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        job_id = str(uuid.uuid4())
        job.timestamp = datetime.now()
        job.status = "submitted"
        job.job_id = job_id
        data = get_data_from_file("jobs.json")
        data.append(job.dict())
        write_data_to_file("jobs.json", data)
        return job_id
    else:
        raise HTTPException(status_code=403, detail="Not allowed")
    
@app.get("/master/jobs/")
async def get_jobs(token:str) -> list:
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        data = get_data_from_file("jobs.json")
        return data
    else:
        raise HTTPException(status_code=403, detail="Not allowed")
    
@app.get("/master/results/")
async def get_results(token:str) -> list:
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        data = get_data_from_file("results.json")
        return data
    else:
        raise HTTPException(status_code=403, detail="Not allowed")

@app.post("/master/result/")
async def create_result(token:str, result:Result):
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        data = get_data_from_file("results.json")
        data.append(result.dict())
        write_data_to_file("results.json", data)
        return result.job_id
    else:
        raise HTTPException(status_code=403, detail="Not allowed")





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)