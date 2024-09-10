import requests

# Your ProxyMesh proxy URL and credentials
proxy = {
    "http": "http://username:password@us-wa.proxymesh.com:31280",
    "https": "http://username:password@us-wa.proxymesh.com:31280",
}

# The target URL you want to scrape
url = "https://www.naukri.com/"

try:
    # Make a request using the proxy
    response = requests.get(url, proxies=proxy)

    # Check if the request was successful
    if response.status_code == 200:
        print("Successfully retrieved the page!")
        print(response.text)  # This will print the HTML content of the page
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
