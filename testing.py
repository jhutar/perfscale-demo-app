from locust import HttpUser, task

class MyAppUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")

    @task
    def get_users(self):
        self.client.get("/api/users")

    @task
    def get_users_uid(self):
        self.client.get("/api/users/1")

    @task
    def get_moves(self):
        self.client.get("/api/moves")

    @task
    def get_moves_mid(self):
        self.client.get("/api/moves/1")
