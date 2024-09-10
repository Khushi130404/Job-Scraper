import requests

# Define the API endpoint and parameters
payload = {
    'api_key': '5e1a841368df1bf578442967a1c3595d',
    'url': 'https://www.glassdoor.com/'
}

# Make the GET request
response = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text', params=payload)

# Print response status and content for debugging
print("Response Status Code:", response.status_code)

# Write the response text to a file
with open('glassdoor.txt', 'w', encoding='utf-8') as file:
    file.write(response.text)
