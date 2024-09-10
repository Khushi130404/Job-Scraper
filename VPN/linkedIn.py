import requests
from requests_html import HTMLSession

# URL to scrape
url = 'https://www.linkedin.com/'

# Start an HTML session
session = HTMLSession()

# Send a GET request to the URL
response = session.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Define the filename to save the HTML content
    filename = 'scraped_linkedin.html'

    # Open the file in write mode and save the HTML content
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"Content successfully saved to {filename}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


