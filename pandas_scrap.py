import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://in.indeed.com/jobs?q=Senior+Research+Analyst&l=Chennai%2C+Tamil+Nadu&start=30&vjk=6379722284897c59"
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(url)
content = driver.page_source
# print(content)

soup = BeautifulSoup(content,'html.parser')
# print(soup)

job_data = soup.find_all("div", class_ = "job_seen_beacon")
# print(job_data)
jobs = []
for job in soup.find_all('div', class_='job_seen_beacon'):
    company_name = job.find('span', class_='css-63koeb eu4oa1w0').text.strip()
    job_title = job.find('h2', class_='jobTitle css-198pbd eu4oa1w0').text.strip()
    location = job.find('div', class_='css-1p0sjhy eu4oa1w0').text.strip()
    responsibilities = [li.text.strip() for li in job.find_all('li')]
    jobs.append({'Company Name': company_name, 'Job Title': job_title, 'Location': location, 'Responsibilities': '\n'.join(responsibilities)})

# Create a pandas DataFrame from the job data
df = pd.DataFrame(jobs)

# Print the DataFrame
print(df)
df.to_csv('indeed_jobs.csv', index=False)
driver.quit()