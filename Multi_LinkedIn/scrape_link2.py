from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import json
import pandas as pd

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Define your LinkedIn credentials
linkedin_username = "khushipatel130404@gmail.com"
linkedin_password = "Khushi1304"

# Navigate to LinkedIn login page
driver.get("https://www.linkedin.com/login")

# Wait for the email and password fields to be present
wait = WebDriverWait(driver, 10)
email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

# Enter your credentials
email_field.send_keys(linkedin_username)
password_field.send_keys(linkedin_password)
password_field.send_keys(Keys.RETURN)

# Wait for login to complete and check if login is successful
time.sleep(10)

# Check for successful login by looking for elements only visible after login
try:
    # Check if the profile icon or home feed is visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Profile']"))
    )
    print("Login successful.")
except:
    print("Login failed. Please check your credentials.")
    driver.quit()
    exit()

# Define the query and base URL for job search
query = "it-jobs"
base_url = f"https://www.linkedin.com/jobs/search/?keywords={query}"
driver.get(base_url)

# Wait for the page to load
time.sleep(10)

# Lists to store data
all_data = []

page = 1
while True:
    # Wait for the page to load and get the page source
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Extract job data
    titles = [title.getText().strip() for title in soup.select("h3.base-search-card__title")]
    company_names_list = [comp.getText().strip() for comp in soup.select("h4.base-search-card__subtitle")]
    locations = [loc.getText().strip() for loc in soup.select("span.job-search-card__location")]
    job_descriptions = [desc.getText().strip() for desc in soup.select("p.job-search-card__snippet")]
    updation_times = [upd.getText().strip() for upd in soup.select("time.job-search-card__listdate")]

    print(f"Titles: {titles}")
    print(f"Company Names: {company_names_list}")
    print(f"Locations: {locations}")
    print(f"Job Descriptions: {job_descriptions}")
    print(f"Updation Times: {updation_times}")

    if not titles:
        print("No data found on this page.")
        break

    # Collect data for the current page
    for title, company, location, desc, updation_time in zip(
            titles, company_names_list, locations, job_descriptions, updation_times):
        job_data = {
            "Job Title": title,
            "Company Name": company,
            "Location": location,
            "Job Description": desc,
            "Updated": updation_time
        }
        all_data.append(job_data)

    print(f"Page {page} data collected")

    # Find and click the "Next" button
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.infinite-scroller__show-more-button"))
        )
        driver.execute_script("arguments[0].click();", next_button)
        page += 1
        time.sleep(5)
    except Exception as e:
        print(f"Error during pagination: {e}")
        break

# Close the driver
driver.quit()

# Check if any data is scraped before saving
if all_data:
    # Save data to CSV
    csv_file = "linkedin_jobs.csv"
    keys = all_data[0].keys()
    with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_data)

    # Save data to Excel
    excel_file = "linkedin_jobs.xlsx"
    df = pd.DataFrame(all_data)
    df.to_excel(excel_file, index=False)

    # Save data to JSON
    json_file = "linkedin_jobs.json"
    with open(json_file, "w", encoding="utf-8") as json_output_file:
        json.dump(all_data, json_output_file, ensure_ascii=False, indent=4)

    print("Data saved to CSV, Excel, and JSON files.")
else:
    print("No data scraped. Exiting without saving.")
