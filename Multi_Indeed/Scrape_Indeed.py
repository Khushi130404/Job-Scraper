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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    job_cards = soup.select("a.jcs-JobTitle")  # Update selector as needed

    for job_card in job_cards:
        try:
            # Extract the link from the job card
            job_link = job_card.get('href')

            # Construct the full URL (ensure it's an absolute URL)
            if job_link.startswith("/"):
                job_link = "https://www.indeed.com" + job_link

            # Click on the job card link
            # driver.execute_script("arguments[0].click();", job_card)
            driver.get(job_link)
            time.sleep(5)  # Wait for the job details to load

            # Get the new page source and parse it with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Extract job details
            title_element = soup.select_one("h1.jobsearch-JobInfoHeader-title")
            title = title_element.get_text(strip=True) if title_element else "No Title Available"

            company_element = soup.select_one("span.jobsearch-JobInfoHeader-companyNameSimple")
            company = company_element.get_text(strip=True) if company_element else "No Company Name Available"

            experience_element = soup.select_one("div.jobsearch-JobComponent-description ul:nth-of-type(5)")
            if experience_element:
                experience = " | ".join([li.get_text(strip=True) for li in experience_element.find_all('li')])
            else:
                experience = "Not Disclosed"

            salary_element = soup.select_one("div.jobsearch-JobMetadataHeader-item.salarySnippet")
            salary = salary_element.get_text(strip=True) if salary_element else "Not Disclosed"

            location_element = soup.select_one("div.js-match-insights-provider-tvvxwd")
            location = location_element.get_text(strip=True) if location_element else "No Location Available"

            description_element = soup.select_one("div.jobsearch-JobComponent-description p:nth-of-type(9)")
            description = description_element.get_text(
                strip=True) if description_element else "No Description Available"

            # Store the job details
            job_data = {
                "Job Title": title,
                "Company Name": company,
                "Experience Required": experience,
                "Salary": salary,
                "Location": location,
                "Job Description": description,
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
    # try:
    #     next_link = driver.find_element(By.CSS_SELECTOR, "a.css-163rxa6")
    #     driver.execute_script("arguments[0].click();", next_link)
    #     if next_link.is_displayed() and next_link.is_enabled():
    #         driver.execute_script("arguments[0].click();", next_link)
    #         page += 1
    #         time.sleep(5)
    #     else:
    #         print("No 'Next' link found or link not clickable. Ending pagination.")
    #         break
    # except Exception as e:
    #     print(f"Error during pagination: {e}")
    #     break

    try:
        # For the 1st page, use the numbered pagination link (e.g., "2")
        if page == 1:
            next_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.css-163rxa6"))
            )
        else:
            # From the 2nd page onwards, use the "Next page" link
            next_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.css-1m2y1qu"))
            )

        driver.execute_script("arguments[0].click();", next_link)
        page += 1
        time.sleep(5)
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
