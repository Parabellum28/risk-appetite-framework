jobs = {}

def create_job(job_id):
    jobs[job_id] = {
        "status": "processing",
        "result": None
    }

def update_job(job_id, result):
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result

def get_job(job_id):
    return jobs.get(job_id)