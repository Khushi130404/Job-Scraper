import scrapy

class NaukriSpider(scrapy.Spider):
    name = 'naukri'
    start_urls = ['https://www.naukri.com/']

    def parse(self, response):
        # Adjust the CSS selectors based on the actual structure of the page
        # Example: Extract job titles from the page
        for job_title in response.css('.title::text').getall():
            yield {'job_title': job_title}

        # Example: Extract job locations if available
        for job_location in response.css('.location::text').getall():
            yield {'job_location': job_location}

        # Follow pagination links if available
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

# scrapy runspider Scrapy/naukri.py -o output.json


# The 403 Forbidden status code indicates that the request to https://www.naukri.com/ was blocked. This can happen for several reasons, including: