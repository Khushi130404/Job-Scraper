import requests


def send_request():
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': 'MIPMIGSMR1QU6FMT3AF6BW23ZJ7TUXYPMMTEZMBT2Q95NE6FHFP65V5KHK3MQTOZSRHVUXPEQDZOPQO1',
            'url': 'https://www.linkedin.com/',  # LinkedIn URL
        },
    )

    print('Response HTTP Status Code: ', response.status_code)

    # Save the response content to a file
    with open('linkedin.txt', 'wb') as file:
        file.write(response.content)
    print('HTML content saved to linkedin.txt')


send_request()
