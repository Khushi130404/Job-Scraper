import scrapy

class FreshersworldSpider(scrapy.Spider):
    name = "freshersworld"
    start_urls = [
        'https://www.freshersworld.com/python-jobs/3535127',
    ]

    def parse(self, response):
        # Extract all job listings from the page
        job_listings = response.css('div.job-container')  # Adjusted to match the outer job container

        for job in job_listings:
            # Extract job details with corrected CSS selectors
            title = job.css('span.wrap-title::text').get(default='').strip()  # Title selector
            company = job.css('h3.company-name::text').get(default='').strip()  # Company name selector
            location = ', '.join(job.css('span.job-location a::text').getall()).strip()  # Combined location selector
            description = job.css('span.desc::text').get(default='').strip()  # Description selector
            experience = job.css('span.experience::text').get(default='').strip()  # Experience
            salary = job.css('span.qualifications::text').get(default='').strip()  # Salary

            # Create a job item dictionary
            job_item = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'experience': experience,
                'salary': salary,
                'link': job.css('div.job-desc-block a::attr(href)').get(default='').strip()  # Link to job details
            }

            yield job_item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)