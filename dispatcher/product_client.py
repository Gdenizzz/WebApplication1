import requests

PRODUCT_SERVICE_URL = "http://127.0.0.1:8002"


def get_products():
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products")

        if response.status_code == 200:
            return response.json()
        else:
            return []

    except Exception as e:
        print("Product service error:", e)
        return []