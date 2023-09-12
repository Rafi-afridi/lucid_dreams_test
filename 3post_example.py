import requests

url = "http://localhost:8000/addPost"

data = {
    "text": "This is my first post"
}

headers = {
    "Authorization": "Bearer 0f77fc333d824a8fcc5fa15e98a41ccff3b63c5f6937b2e5a4536c4ce47508fd"
}

response = requests.post(url, json=data, headers=headers)
# Check the response
if response.status_code == 200:
    print("Post added successfully.")
    print("Response:", response.json())
else:
    print("Error:", response.status_code)
    print("Response:", response.json())
