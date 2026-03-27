import requests

ORDER_SERVICE_URL = "http://127.0.0.1:8003"


def create_order(data):
    try:
        response = requests.post(f"{ORDER_SERVICE_URL}/orders", json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}

    except Exception as e:
        return {"error": str(e)}
    

def get_orders():
    try:
        response = requests.get(f"{ORDER_SERVICE_URL}/orders")

        if response.status_code == 200:
            return response.json()
        else:
            return []

    except Exception as e:
        return []    