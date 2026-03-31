import requests

ORDER_SERVICE_URL = "http://order-service:8002"

def create_order(payload: dict):
    try:
        response = requests.post(f"{ORDER_SERVICE_URL}/orders/", json=payload)
        return response.json()
    except Exception as e:
        print("Order service error:", e)
        return {"error": str(e)}

def get_orders(user_id: str = None):
    try:
        url = f"{ORDER_SERVICE_URL}/orders/"
        if user_id:
            url += f"?user_id={user_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Order service error:", e)
        return []