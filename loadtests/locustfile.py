from locust import HttpUser, task, between, events
import time
import logging
import random
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobQueueUser(HttpUser):

    wait_time = between(0.01, 0.05)

    def on_start(self):
        self.job_ids = []
        response = self.client.get("/health")
        if response.status_code != 200:
            logger.info("Health API is not running")

    @task(10)
    def submit_job(self):
        job_types = ["fast", "slow", "default"]
        job_type = random.choice(job_types)
        payload = {
            "type": job_type,
            "payload": {
                "user_id": random.randint(1,10000),
                "timestamp": int(time.time()),
                "load_test": True,
            }
        }
        with self.client.post("/jobs", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
                job_data = response.json()
                self.job_ids.append(job_data.get("id"))
            else:
                response.failure()

    @task(3)
    def get_job_status(self):
        if self.job_ids:
            job_id = random.choice(self.job_ids[-10:])
            self.client.get(f"/jobs/{job_id}", name="/jobs/[id]")

    @task(2)
    def stats(self):
        self.client.get("/stats", name="[stats]")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("Starting Redis Job Queue load test")
    logger.info("=" *50)

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("Testing complete")
