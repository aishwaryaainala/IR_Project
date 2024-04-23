import os
import scrapy

class PythonOrgSpider(scrapy.Spider):
    name = "python_org"
    start_urls = [
        'https://www.python.org/blogs/',
    ]
    max_pages = 9 # Maximum number of pages to crawl
    max_depth = 5  # Maximum depth of crawling
    output_folder = 'output'  # Folder to store downloaded HTML files

    def parse(self, response):
        # Creating the output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Extracting content and saving HTML to a file in the output folder
        filename = os.path.join(self.output_folder, response.url.split("/")[-2] + '.html')
        with open(filename, 'wb') as f:
            f.write(response.body)

        # Extracting links from the page
        links = response.css('a::attr(href)').getall()

        # Filtering out non-HTML links and controlling maximum pages and depth
        for link in links:
            if link.endswith('.html') and self.max_pages > 0 and response.meta.get('depth', 0) < self.max_depth:
                self.max_pages -= 1
                yield response.follow(link, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})
