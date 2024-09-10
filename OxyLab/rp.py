from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# List of proxies
proxies = [
    "101.255.209.41",
    # "130.61.171.71",
    # "101.255.209.41",
    # "35.185.196.38",
    # "45.119.133.6",
    # "86.57.251.210"
    # "74.208.245.106",
    # "155.54.239.64",
    # "34.124.190.108"
    # "23.95.216.78:34561",
    # "152.42.224.138:3128",
    # "167.99.228.84:3128",
    # "189.240.60.163:9090"  # All proxy forbid
]

# Function to configure WebDriver with a proxy
def get_webdriver_with_proxy(proxy):
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    chrome_options.add_argument("--headless")  # Optional: Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set up the WebDriver (e.g., Chrome)
    service = Service(r'C:\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

# Function to scrape Naukri with a rotating proxy
def scrape_naukri():
    for proxy in proxies:
        driver = None
        try:
            driver = get_webdriver_with_proxy(proxy)
            driver.get("https://www.naukri.com/")

            # Let the page load
            time.sleep(3)

            # Perform job search (e.g., 'Software Engineer')
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'qsb-keyword-sugg'))
            )
            search_box.send_keys('Software Engineer')
            search_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            search_button.click()

            # Wait for the results to load
            time.sleep(5)

            # Parse job titles
            job_titles = driver.find_elements(By.XPATH, "//a[@class='title fw500 ellipsis']")
            for title in job_titles:
                print(title.text.strip())

        except Exception as e:
            print(f"Failed with proxy {proxy}: {e}")

        finally:
            if driver:
                driver.quit()

        # Wait a bit before trying the next proxy
        time.sleep(random.randint(5, 10))

# Start scraping
scrape_naukri()
