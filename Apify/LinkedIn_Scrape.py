import requests
import json


def get_actor_run_output(actor_run_id, token):
    url = f'https://api.apify.com/v2/key-value-stores/zgDx7RHXCuNYPjMO5/records/OUTPUT'
    response = requests.get(url, params={'token': token})

    if response.status_code == 200:
        print('Response HTTP Status Code:', response.status_code)

        # Save the JSON response to a file
        with open('linkedIn.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4)

        print('Response saved to actor_run_output.json')
    else:
        print('Error:', response.status_code, response.text)


# Replace with your actual token and actor run ID
get_actor_run_output('YOUR_ACTOR_RUN_ID', 'YOUR_TOKEN')
