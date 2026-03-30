import requests

PRODUCT_SERVICE_URL = "http://product-service:8001"

def get_products():
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Product service error:", e)
        return []