import requests

AUTH_SERVICE_URL = "http://127.0.0.1:8000"


def verify_token(token: str):
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/verify",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        print("Auth service error:", e)
        return None