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
chrome_options = Options()
# Uncomment if running in headless mode
# chrome_options.add_argument("--headless")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

query = "it-jobs"
base_url = f"https://www.indeed.com/q-{query}-jobs.html"
driver.get(base_url)

# Lists to store data
all_data = []

page = 1
max_pages = 5  # Limit to 5 pages
while page <= max_pages:
    time.sleep(5)  # Wait for the page to load

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all job cards
    job_cards = soup.select("div.job_seen_beacon")  # Update selector as needed

    for job_card in job_cards:
        try:
            # Click on the job card link
            driver.execute_script("arguments[0].click();", job_card)
            time.sleep(5)  # Wait for the job details to load

            # Get the new page source and parse it with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Extract job details
            title = soup.select_one("h1.jobsearch-JobInfoHeader-title").get_text(strip=True)  # Update selector as needed
            company = soup.select_one("div.jobsearch-CompanyInfoWithoutHeaderImage").get_text(strip=True)  # Update selector as needed
            rating = soup.select_one("span.jobsearch-CompanyRating")  # Rating might not be present on every job
            rating = rating.get_text(strip=True) if rating else "No Ratings Available"
            experience = soup.select_one("div.jobsearch-JobMetadataHeader-item")  # Experience might not be available
            experience = experience.get_text(strip=True) if experience else "Not Disclosed"
            salary = soup.select_one("div.jobsearch-JobMetadataHeader-item.salarySnippet")  # Salary might not be available
            salary = salary.get_text(strip=True) if salary else "Not Disclosed"
            location = soup.select_one("div.jobsearch-JobMetadataHeader-item.location")  # Location might not be available
            location = location.get_text(strip=True) if location else "No Location Available"
            description = soup.select_one("div.jobsearch-jobDescriptionText").get_text(strip=True)  # Update selector as needed
            updated = soup.select_one("div.jobsearch-JobMetadataFooter span")  # Last updated time might not be available
            updated = updated.get_text(strip=True) if updated else "No Data Available"

            # Store the job details
            job_data = {
                "Job Title": title,
                "Company Name": company,
                "Ratings": rating,
                "Experience Required": experience,
                "Salary": salary,
                "Location": location,
                "Job Description": description,
                "Updated": updated
            }
            all_data.append(job_data)

            # Go back to the main page
            driver.back()
            time.sleep(5)  # Wait for the main page to reload

        except Exception as e:
            print(f"Error processing job card: {e}")
            driver.back()
            time.sleep(5)

    print(f"Page {page} data collected")

    # Find and click the "Next" link
    try:
        next_link = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
        if next_link.is_displayed() and next_link.is_enabled():
            driver.execute_script("arguments[0].click();", next_link)
            page += 1
            time.sleep(5)
        else:
            print("No 'Next' link found or link not clickable. Ending pagination.")
            break
    except Exception as e:
        print(f"Error during pagination: {e}")
        break

# Close the driver
driver.quit()

# Save data to CSV
csv_file = "job_data.csv"
keys = all_data[0].keys() if all_data else []
with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_data)

# Save data to Excel
excel_file = "job_data.xlsx"
df = pd.DataFrame(all_data)
df.to_excel(excel_file, index=False)

# Save data to JSON
json_file = "job_data.json"
with open(json_file, "w", encoding="utf-8") as json_output_file:
    json.dump(all_data, json_output_file, ensure_ascii=False, indent=4)

print("Data saved to CSV, Excel, and JSON files.")
