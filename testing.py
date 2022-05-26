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
        self.client.get("/api/users/42")

    @task
    def get_users_search_name(self):
        self.client.get("/api/users/search?by=name&text=Petr")

    @task
    def get_users_search_email(self):
        self.client.get("/api/users/search?by=email&text=pavla")

    @task
    def get_users_search_address(self):
        self.client.get("/api/users/search?by=address&text=Brno")

    @task
    def get_moves(self):
        self.client.get("/api/moves")

    @task
    def get_moves_mid(self):
        self.client.get("/api/moves/24")
