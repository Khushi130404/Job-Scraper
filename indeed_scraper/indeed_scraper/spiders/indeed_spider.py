import scrapy

class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    start_urls = [
        "https://www.indeed.com/q-it-jobs-jobs.html"
    ]

    def parse(self, response):
        job_cards = response.css('table.mainContentTable')
        print('Hello.......\n')

        for job_card in job_cards:
            print('Hello.......\n')
            job_url = job_card.css('a.jcs-JobTitle::attr(href)').get(default='').strip()
            job_title = job_card.css('h2.jobTitle a::text').get(default='').strip()
            company = job_card.css('span.company-name::text').get(default='').strip()
            location = job_card.css('div.css-1restlb::text').get(default='').strip()

            # Yield job data directly from the card
            job_item = {
                'title': job_title,
                'company': company,
                'location': location,
                'url': job_url
            }

            yield job_item

        next_page = response.css('a.css-163rxa6::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
