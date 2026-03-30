from locust import HttpUser, task, between

TOKEN = None

class DispatcherUser(HttpUser):
    host = "http://127.0.0.1:8003"
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "http://127.0.0.1:8000/auth/login",
            json={
                "email": "ayse.kaya@gmail.com",
                "password": "Ayse2026!"
            }
        )
        data = response.json()
        self.token = data.get("access_token")

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_products(self):
        self.client.get("/products", headers=self.auth_headers())

    @task(2)
    def get_orders(self):
        self.client.get("/orders", headers=self.auth_headers())

    @task(1)
    def create_order(self):
        self.client.post(
            "/orders",
            json={
                "user_id": "ayse.kaya@gmail.com",
                "items": []
            },
            headers=self.auth_headers()
        )