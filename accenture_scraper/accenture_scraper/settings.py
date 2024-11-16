# Scrapy settings for accenture_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from webdriver_manager.chrome import ChromeDriverManager

BOT_NAME = "accenture_scraper"

SPIDER_MODULES = ["accenture_scraper.spiders"]
NEWSPIDER_MODULE = "accenture_scraper.spiders"

# settings.py
# settings.py

from shutil import which
from selenium.webdriver.chrome.options import Options

# Configure Selenium settings
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')  # Adjust path as needed
# SELENIUM_DRIVER_ARGUMENTS = [
#     '--headless',  # Headless mode for background execution
#     '--user-agent=Custom User-Agent String',  # Custom user agent
#     '--disable-gpu',  # Disable GPU if running in headless mode
#     '--window-size=1200x600'  # Custom window size
# ]
#
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_selenium.SeleniumMiddleware': 800
# }
# Enable Playwright Middleware (Custom Middleware for handling Playwright requests)


# Enable Playwright settings
PLAYWRIGHT_BROWSER_TYPE = 'chromium'  # You can also use 'firefox' or 'webkit' if needed
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,  # Uncomment this line if you want the browser to run in headless mode
    'args': ['--no-sandbox', '--disable-setuid-sandbox'],  # Optional: Use these arguments for headless setup
}

# Additional Playwright options (e.g., slow down, disable animations, etc.)
PLAYWRIGHT_PAGE_TRANSFER = True  # Ensures Playwright pages are correctly transferred



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "accenture_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
TELNETCONSOLE_ENABLED = False

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY =6
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
# Scrapy settings for accenture_scraper project

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 100,
    'accenture_scraper.middlewares.SeleniumMiddleware': 800,
}
LOG_LEVEL: 'ERROR'

# Scrapy settings for Selenium
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = ChromeDriverManager().install()
SELENIUM_DRIVER_ARGUMENTS = ['--headless', '--no-sandbox', '--disable-gpu', '--window-size=1200x600']  # headless mode, adjust if needed
LOG_STDOUT: False

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "accenture_scraper.middlewares.AccentureScraperSpiderMiddleware": 543,
#}
# settings.py


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "accenture_scraper.middlewares.AccentureScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "accenture_scraper.pipelines.AccentureScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
