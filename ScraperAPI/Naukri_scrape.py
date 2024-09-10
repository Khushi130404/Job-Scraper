# ScraperAPI | API Playground
import requests

# Define the API endpoint and parameters
payload = {
    'api_key': '5e1a841368df1bf578442967a1c3595d',
    'url': 'https://www.naukri.com/'
}

# Make the GET request
response = requests.get('https://api.scraperapi.com/', params=payload)

# Print response status and content for debugging
print("Response Status Code:", response.status_code)

# Write the response text to a file
with open('naukri.txt', 'w', encoding='utf-8') as file:
    file.write(response.text)
