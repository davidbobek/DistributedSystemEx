from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
import json
import uuid
import datetime
from users import get_role
from schemas import Job, Result, JobSubmit, ResultSubmit, Status
from auth import AuthHandler

app = FastAPI()
security = HTTPBearer()
authHandler = AuthHandler()

allowed_roles = ["Administrator", "Manager"]


    
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

        
@app.post("/master/job/")
async def create_job(token:str, job:JobSubmit) -> str:
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        for a in job.assets:
            # check if asser > 100 or < 0 and int
            if not isinstance(a, int) or a > 100 or a < 0:
                raise HTTPException(status_code=400, detail="Invalid asset value")
        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        data = get_data_from_file("jobs.json")
        job = Job(id=f"job_{len(data)}", user=username, timestamp=timestamp, status=Status.Submitted, date_range=job.date_range, assets=job.assets)
        data.append(job.__dict__)
        write_data_to_file("jobs.json", data)
        return job.id
    else:
        raise HTTPException(status_code=403, detail="Not allowed")
    
@app.get("/master/jobs/")
async def get_jobs(token:str) -> list:
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        return get_data_from_file("jobs.json")
    else:
        raise HTTPException(status_code=403, detail="Not allowed")
    

@app.put("/master/job/<job_id>")
async def update_result(token:str, job_id:str) -> int:
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        jobs = get_data_from_file("jobs.json")
        if not jobs:
            raise HTTPException(status_code=404, detail="Jobs not found")
        if job_id not in [job["id"] for job in jobs]:
            raise HTTPException(status_code=404, detail="Job not found")
        for job in jobs:
            if job["id"] == job_id:
                job["status"] = Status.Processing
        write_data_to_file("jobs.json", jobs)
        return 200
    else:
        raise HTTPException(status_code=403, detail="Not allowed")

    
@app.get("/master/results/")
async def get_results(token:str) -> list:
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        return get_data_from_file("results.json")
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


@app.post("/master/result/")
async def create_result(token:str, result:ResultSubmit):
    username = authHandler.decode_token(token)
    if get_role(username) in allowed_roles:
        data = get_data_from_file("jobs.json")
        job = [job for job in data if job["id"] == result.job_id][0]
        assert_len = len(job['assets'])
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job["status"] == Status.Done:
            raise HTTPException(status_code=400, detail="Job already done")
        assert_len = len(job['assets'])
        if len(result.assets) != assert_len:
            raise HTTPException(status_code=400, detail="Wrong number of assets")
        job["status"] = Status.Done
        write_data_to_file("jobs.json", data)
        data = get_data_from_file("results.json")
        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        result = Result(job_id=result.job_id, assets=result.assets, timestamp=timestamp)
        data.append(result.__dict__)
        write_data_to_file("results.json", data)
        return result.job_id
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)