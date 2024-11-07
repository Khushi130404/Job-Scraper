import scrapy

class FreshersworldSpider(scrapy.Spider):
    name = "freshersworld"
    start_urls = [
        'https://www.accenture.com/us-en/careers/jobsearch?jk=it-jobs',
    ]

    def parse(self, response):
        # Extract all job listings from the page
        job_listings = response.css('div.rad-filters-vertical__job-card-header')  # Adjusted to match the outer job container

        for job_card in job_listings:
            # Extract job details with corrected CSS selectors
            title = job_card.css("h3.rad-filters-vertical__job-card-title::text").get(default="N/A").strip()
            location = job_card.css("span.rad-filters-vertical__job-card-details-location::text").get(
                default="N/A").strip()
            description = job_card.css(
                "span.rad-filters-vertical__job-card-content-standard-title-dynamic-text::text").get(
                default="N/A").strip()
            experience = job_card.css("span.rad-filters-vertical__job-card-details-type::text").get(
                default="Experience details not available").strip()

            # Create a job item dictionary
            job_item = {
                'title': title,
                'location': location,
                'description': description,
                'experience': experience,
                'link': job_card.css('div.job-desc-block a::attr(href)').get(default='').strip()  # Link to job details
            }

            yield job_item

        next_page = response.css("a.rad-pagination__page-number-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)