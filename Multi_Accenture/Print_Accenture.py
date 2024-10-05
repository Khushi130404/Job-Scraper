from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import json
import pandas as pd

# Initialize Chrome options
chrome_options = Options()
# Uncomment the following line if you want to run in headless mode
# chrome_options.add_argument("--headless")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

query = "it-jobs"
base_url = f"https://www.accenture.com/us-en/careers/jobsearch?jk={query}"
driver.get(base_url)

# Lists to store data
all_data = []

# Counter for pages
page_counter = 0
max_pages = 5

while page_counter < max_pages:
    time.sleep(5)  # Wait for the page to load

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all job titles
    titles = soup.select("h3.rad-filters-vertical__job-card-title")
    titles_list = [title.getText().strip() for title in titles]

    # Ensure there are titles to process
    if not titles_list:
        print("No job titles found. Exiting.")
        break

    # Find locations, job descriptions, and experience requirements
    locations = soup.select("span.rad-filters-vertical__job-card-details-location")  # Update this selector
    locations_list = [location.getText().strip() for location in locations] or ["N/A"] * len(titles_list)

    job_descriptions = soup.select("span.rad-filters-vertical__job-card-content-standard-title-dynamic-text")  # Update this selector
    job_descriptions_list = [desc.getText().strip() for desc in job_descriptions] or ["N/A"] * len(titles_list)

    experience_list = [exp.getText().strip() if exp else "Experience details not available" for exp in soup.select("span.rad-filters-vertical__job-card-details-type")] or ["N/A"] * len(titles_list)

    # Debug print statements
    print(f"Page {page_counter + 1} URL: {driver.current_url}")
    print(f"Titles: {titles_list}")
    print(f"Locations: {locations_list}")
    print(f"Descriptions: {job_descriptions_list}")
    print(f"Experiences: {experience_list}")


    for index, (title, location, desc, experience) in enumerate(zip(titles_list, locations_list, job_descriptions_list, experience_list), start=1):
        job_data = {
            "Job Title": title,
            "Location": location,
            "Job Description": desc,
            "Experience Required": experience
        }
        print(json.dumps(job_data, ensure_ascii=False, indent=4))

    print(f"Page {page_counter + 1} data collected")

    # Find and click the "Next" link
    try:
        next_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.rad-pagination__page-number:not(.rad-pagination__page-number--selected)"))
        )
        driver.execute_script("arguments[0].click();", next_link)
        page_counter += 1
        time.sleep(3)
    except Exception as e:
        print(f"Error during pagination: {e}")
        break

driver.quit()
