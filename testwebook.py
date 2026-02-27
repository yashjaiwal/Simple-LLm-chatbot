import requests

user_message = "Hi how are you"

request_message = {
    "message": user_message
}

url = "http://localhost:5678/webhook-test/90592a4f-e0af-44de-bcc4-f57b2c3b6c5d"

response = requests.post(url, json=request_message)

print(response.status_code)
print(response.text)