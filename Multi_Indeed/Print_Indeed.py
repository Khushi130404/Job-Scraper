from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
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

# Lists to store pagination links
pagination_links = []

# Step 1: Scrape pagination links (2, 3, 4, 5)
try:
    # Wait for the pagination elements to load and collect their URLs
    pagination_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.css-163rxa6"))
    )
    for elem in pagination_elements:
        pagination_links.append(elem.get_attribute('href'))
except Exception as e:
    print(f"Error getting pagination links: {e}")


# Step 2: Scrape the data from the current page
def scrape_page():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    job_cards = soup.select("a.jcs-JobTitle")  # Update selector as needed
    for job_card in job_cards:
        try:
            job_link = job_card.get('href')
            if job_link.startswith("/"):
                job_link = "https://www.indeed.com" + job_link
            driver.get(job_link)
            time.sleep(5)

            # Get the new page source and parse it
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            title_element = soup.select_one("h1.jobsearch-JobInfoHeader-title")
            title = title_element.get_text(strip=True) if title_element else "No Title Available"

            company_element = soup.select_one("a.css-1ioi40n")
            company = company_element.get_text(strip=True) if company_element else "No Company Name Available"

            experience_element = soup.select_one("div.jobsearch-JobComponent-description ul:nth-of-type(5)")
            experience = " | ".join([li.get_text(strip=True) for li in
                                     experience_element.find_all('li')]) if experience_element else "Not Disclosed"

            salary_element = soup.select_one("div.js-match-insights-provider-tvvxwd")
            salary = salary_element.get_text(strip=True) if salary_element else "Not Disclosed"

            location_element = soup.select_one("div.css-1ojh0uo")
            location = location_element.get_text(strip=True) if location_element else "No Location Available"

            # Try to extract job description from a <p> tag first
            description_element = soup.select_one("div.jobsearch-JobComponent-description p:nth-of-type(1)")

            # If the <p> tag is not available, fall back to the first <ul> and collect all <li> items
            if description_element:
                description = description_element.get_text(strip=True)
            else:
                # Check for a <ul> with <li> elements
                description_list = soup.select_one("div.jobsearch-JobComponent-description ul:nth-of-type(1)")
                if description_list:
                    description = " | ".join([li.get_text(strip=True) for li in description_list.find_all('li')])
                else:
                    description = "No Description Available"

            job_data = {
                "Job Title": title,
                "Company Name": company,
                "Experience Required": experience,
                "Salary": salary,
                "Location": location,
                "Job Description": description,
            }

            # Print the job data as it is scraped
            print(json.dumps(job_data, ensure_ascii=False, indent=4))

            driver.back()
            time.sleep(5)
        except Exception as e:
            print(f"Error processing job card: {e}")
            driver.back()
            time.sleep(5)


# Scrape the current (first) page
scrape_page()
print("Page 1 data collected")

# Step 3: Iterate through pagination links and scrape subsequent pages
for i, page_url in enumerate(pagination_links):
    try:
        driver.get(page_url)
        time.sleep(5)
        scrape_page()
        print(f"Page {i + 2} data collected")  # Because page 1 is already scraped
    except Exception as e:
        print(f"Error scraping page {i + 2}: {e}")

# Close the driver
driver.quit()
