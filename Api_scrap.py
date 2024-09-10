# import requests
#
# api_url = "https://jsonplaceholder.typicode.com/posts"
# response = requests.get(api_url)
#
# if response.status_code == 200:
#     data = response.json()
#     for post in data:
#         print(f"Post ID: {post['id']}")
#         print(f"Title: {post['title']}")
#         print(f"Body: {post['body']}")
#         print("------")
# else:
#     print(f"Failed to retrieve data: {response.status_code} - {response.text}")

import requests
import pandas as pd

api_url = "https://api.example.com/jobs"
querystring = {
    "query": "Senior Research Analyst",
    "location": "Chennai"
}
headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}

response = requests.get(api_url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()
    jobs = data.get('jobs', [])
    job_list = []

    for job in jobs:
        job_list.append({
            'Company Name': job.get('company', 'N/A'),
            'Job Title': job.get('title', 'N/A'),
            'Location': job.get('location', 'N/A'),
            'Salary': job.get('salary', 'N/A')
        })

    df = pd.DataFrame(job_list)
    df.to_csv('api_jobs.csv', index=False)

    print("Data saved to api_jobs.csv")
else:
    print(f"Failed to retrieve data: {response.status_code} - {response.text}")
