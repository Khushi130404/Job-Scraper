import requests

# Public API endpoint
url = "https://jsonplaceholder.typicode.com/posts"

# Making the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    for post in data:
        print(f"Post ID: {post['id']}, Title: {post['title']}")
else:
    print(f"Request failed with status code: {response.status_code}")