import scrapy
from urllib.parse import urljoin

class AccentureSpider(scrapy.Spider):
    name = "accenture_spider"
    start_urls = [
        'https://www.accenture.com/us-en/careers/jobsearch?jk=it-jobs',
    ]

    def parse(self, response):
        job_listings = response.css('div.rad-filters-vertical__job-card')
        print(f"Found {len(job_listings)} job listings")

        for job_card in job_listings:
            print("Job Card HTML:", job_card.get())  # Print the HTML of each job card to confirm structure
            title = job_card.css("h3.rad-filters-vertical__job-card-title::text").get(default="N/A").strip()
            location = job_card.css("div.rad-filters-vertical__job-card-header div.rad-filters-vertical__job-card-details span.rad-filters-vertical__job-card-details-location::text").get(default="N/A").strip()
            description = job_card.css("span.rad-filters-vertical__job-card-details-schedule::text").get(
                default="N/A").strip()
            experience = job_card.css("span.rad-filters-vertical__job-card-details-type::text").get(
                default="Experience details not available").strip()

            print(f"Title: {title}, Location: {location}, Description: {description}, Experience: {experience}")

            # Construct the full link to job details
            link = job_card.css('div.job-desc-block a::attr(href)').get(default='').strip()
            full_link = urljoin(response.url, link) if link else 'N/A'

            # Create a job item dictionary, saving even if fields are N/A
            job_item = {
                'title': title,
                'location': location,
                'description': description,
                'experience': experience,
                'link': full_link
            }

            # Yield the item (Scrapy will handle saving it based on your output settings, e.g., to a CSV, JSON, or database)
            yield job_item

        # Follow pagination link to the next page if available
        next_page = response.css("a.rad-pagination__page-number-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
