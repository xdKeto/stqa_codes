from locust import HttpUser, task, between

class HitCounterUser(HttpUser):
    host = "http://localhost:5000"
    wait_time = between(3, 5)
    
    @task(3)
    def post_hit(self):
        self.client.post("/hit")
    
    @task(1)
    def load_homepage(self):
        self.client.get("/")
        
    
        