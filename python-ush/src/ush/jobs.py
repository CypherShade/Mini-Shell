class Job:
    def __init__(self, job_id, command, process):
        self.job_id = job_id
        self.command = command
        self.process = process
        self.status = 'running'

    def is_completed(self):
        return self.process.poll() is not None

    def update_status(self):
        if self.is_completed():
            self.status = 'completed'
        else:
            self.status = 'running'


class JobManager:
    def __init__(self):
        self.jobs = {}
        self.next_job_id = 1

    def add_job(self, command, process):
        job = Job(self.next_job_id, command, process)
        self.jobs[self.next_job_id] = job
        self.next_job_id += 1
        return job.job_id

    def remove_job(self, job_id):
        if job_id in self.jobs:
            del self.jobs[job_id]

    def get_jobs(self):
        return {job_id: job for job_id, job in self.jobs.items() if not job.is_completed()}

    def update_jobs(self):
        for job in self.jobs.values():
            job.update_status()