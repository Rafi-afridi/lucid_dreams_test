import requests

url = "http://localhost:8000/login"

data = {
    "email": "user@example.com",
    "password": "securepassword"
}

# Replace 'your_token_here' with the actual token obtained from login/signup
headers = {
    "Authorization": "Bearer 0f77fc333d824a8fcc5fa15e98a41ccff3b63c5f6937b2e5a4536c4ce47508fd"
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.json()) 