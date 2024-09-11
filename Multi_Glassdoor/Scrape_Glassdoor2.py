from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import csv
import json
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Chrome options
chrome_options = Options()
# Uncomment if running in headless mode
# chrome_options.add_argument("--headless")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

query = "it-jobs"
base_url = f"https://www.glassdoor.co.in/Job/{query}-jobs-SRCH_KO0,8.htm"
driver.get(base_url)

# Lists to store data
all_data = []

def random_sleep():
    time.sleep(random.uniform(10, 15))

# Function to click the "Load More" button if available
def click_load_more():
    try:
        # Use the updated selector for the "Show more jobs" button
        load_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test='load-more']"))
        )
        if load_more_button:
            load_more_button.click()
            time.sleep(5)  # Adjust this based on page load time
            print("Clicked 'Show more jobs' button")
            return True
    except Exception as e:
        print(f"No 'Show more jobs' button found or error occurred: {e}")
    return False

# Step 1: Scrape the data from the current page
def scrape_page():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    job_cards = soup.select("a[data-test='job-link']")  # Update selector as per the provided structure
    for job_card in job_cards:
        try:
            job_link = job_card.get('href')
            if job_link and job_link.startswith("/"):
                job_link = "https://www.glassdoor.co.in" + job_link
            print(f"Visiting job link: {job_link}")
            driver.get(job_link)
            random_sleep()  # Wait for the page to load
            # Get the new page source and parse it
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            title_element = soup.select_one("h1.heading_Heading__BqX5J")
            title = title_element.get_text(strip=True) if title_element else "No Title Available"

            company_element = soup.select_one("h4.heading_Heading__BqX5J")
            company = company_element.get_text(strip=True) if company_element else "No Company Name Available"

            location_element = soup.select_one("div.JobDetails_jobDescription_uW_fK p:nth-of-type(8)")
            location = location_element.get_text(strip=True) if location_element else "No Location Available"

            salary_element = soup.select_one("div.JobDetails_jobDescription_uW_fK p:nth-of-type(4)")
            salary = salary_element.get_text(strip=True) if salary_element else "Not Disclosed"

            experience_list = soup.select_one("div.JobDetails_jobDescription_uW_fK ul:nth-of-type(2)")
            if experience_list:
                experience = " | ".join([li.get_text(strip=True) for li in experience_list.find_all('li')])
            else:
                experience = "No Description Available"

            description_list = soup.select_one("div.JobDetails_jobDescription_uW_fK ul:nth-of-type(1)")
            if description_list:
                description = " | ".join([li.get_text(strip=True) for li in description_list.find_all('li')])
            else:
                description = "No Description Available"

            rating_element = soup.select_one("div.Rating_Headline_sectionRatingScoreLeft_di1of")
            rating = rating_element.get_text(strip=True) if rating_element else "No Rating"

            job_data = {
                "Job Title": title,
                "Company Name": company,
                "Location": location,
                "Salary": salary,
                "Experience" : experience,
                "Job Description": description,
                "Ratings" : rating
            }
            all_data.append(job_data)

            driver.back()
            time.sleep(5)
        except Exception as e:
            print(f"Error processing job card: {e}")
            driver.back()
            time.sleep(5)

# Scrape the current page
scrape_page()
print("Initial page data collected")

# Limit the number of "Load More" clicks
max_clicks = 1
click_count = 0

# Click 'Load More' and scrape additional pages, up to the max_clicks limit
while click_count < max_clicks and click_load_more():
    scrape_page()
    click_count += 1

# Close the driver
driver.quit()

# Save data to CSV, Excel, and JSON files
csv_file = "glassdoor_job_data.csv"
keys = all_data[0].keys() if all_data else []
with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_data)

excel_file = "glassdoor_job_data.xlsx"
df = pd.DataFrame(all_data)
df.to_excel(excel_file, index=False)

json_file = "glassdoor_job_data.json"
with open(json_file, "w", encoding="utf-8") as json_output_file:
    json.dump(all_data, json_output_file, ensure_ascii=False, indent=4)

print("Data saved to CSV, Excel, and JSON files.")
