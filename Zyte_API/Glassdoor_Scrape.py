from base64 import b64decode
import requests

# Make the POST request to Zyte API
api_response = requests.post(
    "https://api.zyte.com/v1/extract",
    auth=("d6417cfbdaa84545a7651911d139bafe", ""),
    json={
        "url": "https://www.glassdoor.com/",
        "httpResponseBody": True,
    },
)

# Decode the HTTP response body from base64
http_response_body: bytes = b64decode(api_response.json()["httpResponseBody"])

# Write the decoded response body to a file
with open('glassdoor.html', 'wb') as file:
    file.write(http_response_body)
