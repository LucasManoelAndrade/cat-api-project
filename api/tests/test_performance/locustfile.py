from locust import HttpUser, task, between

class CatApiUser(HttpUser):
    wait_time = between(1, 3)  # segundos entre requisições simuladas

    @task(3)
    def get_all_breeds(self):
        self.client.get("/cats/breeds")

    @task(1)
    def get_breeds_by_origin(self):
        self.client.get("/cats/breeds/origin/Egypt")

    @task(1)
    def get_breeds_by_temperament(self):
        self.client.get("/cats/breeds/temperament/Playful")

    @task(1)
    def get_breed_by_name(self):
        self.client.get("/cats/breeds/name/Abyssinian")
