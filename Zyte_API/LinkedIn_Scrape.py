from base64 import b64decode
import requests

# Make the POST request to Zyte API
api_response = requests.post(
    "https://api.zyte.com/v1/extract",
    auth=("d6417cfbdaa84545a7651911d139bafe", ""),
    json={
        "url": "https://www.linkedin.com/",
        "httpResponseBody": True,
    },
)

# Print the status code for debugging
print("Status Code:", api_response.status_code)

# Print the entire JSON response for debugging
print("Response JSON:", api_response.json())

# Decode the HTTP response body if it exists
if "httpResponseBody" in api_response.json():
    http_response_body: bytes = b64decode(api_response.json()["httpResponseBody"])
    with open('linkedin.txt', 'wb') as file:
        file.write(http_response_body)
else:
    print("Error: 'httpResponseBody' not found in the response.")
    print(api_response.json())  # Print the full response to understand the error

# C:\Users\Khushi\PycharmProjects\Scraping1\.venv\Scripts\python.exe C:\Users\Khushi\PycharmProjects\Scraping1\Zyte_API\LinkedIn_Scrape.py
# Status Code: 451
# Response JSON: {'blockedDomain': 'linkedin.com', 'type': '/download/domain-forbidden', 'title': 'Domain Forbidden', 'status': 451, 'detail': 'Extraction for the domain linkedin.com is forbidden.'}
# Error: 'httpResponseBody' not found in the response.
# {'blockedDomain': 'linkedin.com', 'type': '/download/domain-forbidden', 'title': 'Domain Forbidden', 'status': 451, 'detail': 'Extraction for the domain linkedin.com is forbidden.'}
#
# Process finished with exit code 0