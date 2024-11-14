import scrapy

class ShineSpider(scrapy.Spider):
    name = "shine_spider"
    start_urls = [
        'https://www.shine.com/job-search/it-jobs/',
    ]
    max_pages = 5  # Set the maximum number of pages to scrape
    page_counter = 1  # Track the current page count

    def parse(self, response):
        job_listings = response.css('div.jobCard_jobCard__jjUmu')

        for job in job_listings:
            # Extract job details with corrected CSS selectors
            title = job.css('strong.jobCard_pReplaceH2__xWmHg p a::text').get(default='').strip()  # Title selector
            link = job.css('strong.jobCard_pReplaceH2__xWmHg p a::attr(href)').get(default='').strip()  # Job link selector
            company = job.css('div.jobCard_jobCard_cName__mYnow span::text').get(default='').strip()  # Company name selector
            location = ', '.join(job.css('div.jobCard_locationIcon__zrWt2::text').getall()).strip()  # Combined location selector
            description = job.css('div.jobCard_skillList__KKExE::text').get(default='').strip()  # Description selector
            experience = job.css('div.jobCard_jobIcon__3FB1t::text').get(default='').strip()  # Experience

            # Create a job item dictionary
            job_item = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'experience': experience,
                'link': link
            }

            yield job_item

        # Pagination handling
        if self.page_counter < self.max_pages:
            next_page = response.css('div.jsrpcomponent_pagination__gBo0y a::attr(href)').getall()[-1]
            if next_page:
                self.page_counter += 1  # Increase page count
                yield response.follow(next_page, callback=self.parse)
