from locust import HttpUser, task

class MyAppUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")

    @task
    def get_users(self):
        self.client.get("/api/users")

    @task
    def get_moves(self):
        self.client.get("/api/moves")
