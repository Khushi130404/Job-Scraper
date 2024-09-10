from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Single proxy to test
# proxy = "154.65.39.7:80"
# proxy = "189.240.60.168:9090"
# proxy = "35.185.196.38:3128"
# proxy = "23.95.216.78:34561"
# proxy = "152.42.224.138:3128"
# proxy = "167.99.228.84:3128"
proxy = "189.240.60.163:9090"

def get_glassdoor_jobs(query, location):
    # Set up Selenium with ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set the proxy
    chrome_options.add_argument(f'--proxy-server={proxy}')

    # Path to ChromeDriver executable
    service = ChromeService(executable_path=r'C:\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locT=C&locId=1147441"
    # url = f"https://www.naukri.com/{query}-jobs-in-{location}"
    driver.get(url)

    # Print page title to confirm page load
    print("Page title:", driver.title)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "react-job-listing"))
        )
    except Exception as e:
        print(f"Failed to load job listings: {e}")
        driver.quit()
        return []

    job_cards = driver.find_elements(By.CLASS_NAME, "react-job-listing")

    # Print number of job cards found
    print("Number of job cards found:", len(job_cards))

    jobs = []
    for job_card in job_cards:
        try:
            company = job_card.find_element(By.CLASS_NAME, 'jobHeader').text.strip()
            title = job_card.find_element(By.CLASS_NAME, 'jobLink').text.strip()
            location = job_card.find_element(By.CLASS_NAME, 'loc').text.strip() if job_card.find_element(By.CLASS_NAME,
                                                                                                         'loc') else 'N/A'
            salary = job_card.find_element(By.CLASS_NAME, 'css-56kyx5').text.strip() if job_card.find_element(
                By.CLASS_NAME, 'css-56kyx5') else 'N/A'
        except Exception as e:
            print(f"Error extracting job details: {e}")
            continue

        jobs.append({
            'Company Name': company,
            'Job Title': title,
            'Location': location,
            'Salary': salary
        })

    driver.quit()
    return jobs


query = "Senior Research Analyst"
location = "Chennai"

jobs = get_glassdoor_jobs(query, location)

if jobs:
    df = pd.DataFrame(jobs)
    df.to_csv('glassdoor_jobs.csv', index=False)
    print("Data saved to glassdoor_jobs.csv")
else:
    print("No jobs found or failed to retrieve data")
