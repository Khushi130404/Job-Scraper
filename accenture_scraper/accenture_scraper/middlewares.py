import logging
from scrapy.http import HtmlResponse
from selenium import webdriver
from scrapy.utils.project import get_project_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class SeleniumMiddleware:
    """Scrapy middleware handling requests using Selenium"""

    def __init__(self):
        self.driver = None
        settings = get_project_settings()
        self.driver_path = settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""
        options = webdriver.ChromeOptions()
        for arg in spider.settings.get('SELENIUM_DRIVER_ARGUMENTS', []):
            options.add_argument(arg)

        # Initialize the driver if it's not already
        if self.driver is None:
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=options)

        self.driver.get(request.url)

        # Wait until the page is loaded (you can customize the wait condition)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
        )

        # Grab the page source after it's loaded
        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute so the spider can access it
        request.meta.update({"driver": self.driver})

        # Return the HTML response to be parsed by Scrapy
        return HtmlResponse(
            url=request.url, body=body, encoding="utf-8", request=request
        )
