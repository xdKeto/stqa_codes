import random
import time
from turtle import st

from locust import HttpUser, SequentialTaskSet, between, task

RESPONSE_TIME_LIMIT_MS = 3000.0

class PetShopWorkflow(SequentialTaskSet):

    @task
    def add_new_pet(self):
        pet_name = f"Fluffy{random.randint(1, 10000)}"

        self.client.post("/pets", json={"name": pet_name, "category": "dog"})


    @task
    def load_home_page(self):
        start_time = time.time()
        
        with self.client.get("/", catch_response=True) as response:
            response_time_ms = (time.time() - start_time) * 1000
            
            if response_time_ms > RESPONSE_TIME_LIMIT_MS:
                response.failure(f"Response time exceeded limit of {RESPONSE_TIME_LIMIT_MS} ms")
            elif response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                response.success()
        
        # self.client.get("/")
        
        
class PetShopUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time= between(0, 0)
    tasks = [PetShopWorkflow]
    
