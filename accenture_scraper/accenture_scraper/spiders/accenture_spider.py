import scrapy
from scrapy.http import HtmlResponse
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

class AccentureSpider(scrapy.Spider):
    name = "accenture_spider"
    start_urls = ['https://www.accenture.com/us-en/careers/jobsearch?jk=it-jobs']
    max_pages = 5  # Limit the number of pages to scrape
    page_counter = 0
    all_data = []

    def start_requests(self):
        # Yield a dummy request to pass control to the `parse` method
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # Initialize Chrome options
        options = Options()
        options.add_argument("--headless")  # Headless mode

        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(self.start_urls[0])
        time.sleep(2)  # Wait for the page to load

        # Process the first page
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        self.extract_and_save_data(soup)

        # Handle pagination
        while self.page_counter < self.max_pages:
            try:
                # Find the "Next" button and click it
                next_page = driver.find_element(By.CSS_SELECTOR,
                    "button.rad-pagination__page-number:not(.rad-pagination__page-number--selected)")
                driver.execute_script("arguments[0].click();", next_page)
                self.page_counter += 1
                time.sleep(3)  # Wait for the page to load

                # Get the new page source and parse it
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                self.extract_and_save_data(soup)

            except Exception as e:
                self.logger.error(f"Error during pagination: {e}")
                break

        # Close the driver
        driver.quit()

        # Save data to CSV, Excel, and JSON
        if self.all_data:
            self.save_data(self.all_data)

    def extract_and_save_data(self, soup):
        titles = soup.select("h3.rad-filters-vertical__job-card-title")
        titles_list = [title.getText().strip() for title in titles]

        if not titles_list:
            self.logger.info("No job titles found. Exiting.")
            return

        locations = soup.select("span.rad-filters-vertical__job-card-details-location")
        locations_list = [location.getText().strip() for location in locations] or ["N/A"] * len(titles_list)

        job_descriptions = soup.select("span.rad-filters-vertical__job-card-content-standard-title-dynamic-text")
        job_descriptions_list = [desc.getText().strip() for desc in job_descriptions] or ["N/A"] * len(titles_list)

        experience_list = [exp.getText().strip() if exp else "Experience details not available" for exp in
                           soup.select("span.rad-filters-vertical__job-card-details-type")] or ["N/A"] * len(titles_list)

        for title, location, desc, experience in zip(titles_list, locations_list, job_descriptions_list, experience_list):
            job_data = {
                "Job Title": title,
                "Location": location,
                "Job Description": desc,
                "Experience Required": experience
            }
            self.all_data.append(job_data)

        self.logger.info(f"Page {self.page_counter + 1} data collected")

    def save_data(self, data):
        csv_file = "job_data_2.csv"
        keys = data[0].keys()
        with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

        excel_file = "job_data_2.xlsx"
        df = pd.DataFrame(data)
        df.to_excel(excel_file, index=False)

        json_file = "job_data_2.json"
        with open(json_file, "w", encoding="utf-8") as json_output_file:
            json.dump(data, json_output_file, ensure_ascii=False, indent=4)

        self.logger.info("Data saved to CSV, Excel, and JSON files.")
