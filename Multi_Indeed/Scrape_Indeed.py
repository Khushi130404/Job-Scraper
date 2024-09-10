from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import json
import pandas as pd

# Initialize Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

query = "it jobs"
base_url = f"https://www.indeed.com/q-{query.replace(' ', '-')}"
driver.get(base_url)

# Lists to store data
all_data = []

page = 1
while True:
    time.sleep(5)  # Wait for the page to load

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all job titles
    titles = soup.select("h2.jobTitle")
    titles_list = [title.getText().strip() for title in titles]

    # Find company names
    companies = soup.select("span.companyName")
    company_names_list = [company.getText().strip() for company in companies]

    # Find ratings
    ratings = soup.select("span.ratingNumber")
    ratings_list = [rating.getText().strip() if rating else "No Rating" for rating in ratings]

    # Find experience requirements (not always available)
    experiences = soup.select("div.job-snippet")
    experience_list = [exp.getText().strip() if exp else "Not Disclosed" for exp in experiences]

    # Find salaries (may not always be available)
    salaries = soup.select("span.salary-snippet")
    salaries_list = [salary.getText().strip() if salary else "Not Disclosed" for salary in salaries]

    # Find locations
    locations = soup.select("div.companyLocation")
    locations_list = [location.getText().strip() for location in locations]

    # Find job descriptions (may need adjustment based on availability)
    descriptions = soup.select("div.job-snippet")
    descriptions_list = [desc.getText().strip() for desc in descriptions]

    # Find posting dates
    posting_dates = soup.select("span.date")
    posting_dates_list = [date.getText().strip() for date in posting_dates]

    # Collect data for the current page
    page_data = []
    for title, company, rating, experience, salary, location, desc, posting_date in zip(
            titles_list, company_names_list, ratings_list, experience_list, salaries_list, locations_list,
            descriptions_list, posting_dates_list):
        job_data = {
            "Job Title": title,
            "Company Name": company,
            "Ratings": rating,
            "Experience Required": experience,
            "Salary": salary,
            "Location": location,
            "Job Description": desc,
            "Posting Date": posting_date
        }
        page_data.append(job_data)
        all_data.append(job_data)

    print(f"Page {page} data collected")

    # Find and click the "Next" link
    try:
        next_link = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
        if next_link.is_displayed() and next_link.is_enabled():
            driver.execute_script("arguments[0].click();", next_link)
            page += 1
            time.sleep(3)
        else:
            print("No 'Next' link found or link not clickable. Ending pagination.")
            break
    except Exception as e:
        print(f"Error during pagination: {e}")
        break

# Close the driver
driver.quit()

# Save data to CSV
csv_file = "indeed_job_data.csv"
keys = all_data[0].keys()
with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_data)

# Save data to Excel
excel_file = "indeed_job_data.xlsx"
df = pd.DataFrame(all_data)
df.to_excel(excel_file, index=False)

# Save data to JSON
json_file = "indeed_job_data.json"
with open(json_file, "w", encoding="utf-8") as json_output_file:
    json.dump(all_data, json_output_file, ensure_ascii=False, indent=4)

print("Data saved to CSV, Excel, and JSON files.")
