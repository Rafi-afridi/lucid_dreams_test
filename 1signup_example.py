import requests

url = "http://localhost:8000/signup"

data = {
    "email": "user@example.com",
    "password": "securepassword"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())  # This will contain the user's token