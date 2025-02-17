# Import the required libraries
from src import logger
from bs4 import BeautifulSoup
from src.web_scraping.WebScraper import WebScraper


class DataExtractor:

    def extract_data(self, url):
        """
        This function extracts data from the specified URL.
        :param url: The URL of the website to extract data from.
        :return: A dictionary containing the extracted data and the article titles as keys.
        """

        # Fetch the raw HTML content
        logger.info(f"Fetching content from {url}")
        html_content = WebScraper().scraper(url)

        # Parse the HTML content
        logger.info("Parsing the HTML content.")
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all listing elements
        logger.info("Finding all listing elements.")
        listings = soup.find_all('listing-with-preview')

        # Initialize the data dictionary
        data = dict()

        # Extract data
        for listing in listings:

            # content_type = listing.get('content-type-name', 'Unknown').strip()
            # publish_date = listing.get('publish-date-ap', 'Unknown').strip()
            # summary = listing.get('article-summary', 'Unknown').strip()

            # Extract the title and article URL
            logger.info("Extracting title and article URL.")
            title = listing.get('article-title', None).strip()
            article_url = listing.get('article-url', None).strip()

            # Skip if either the title or article URL is missing
            if title and article_url:

                # Call the scraper function to get the content of the article URL
                text = WebScraper().get_content(article_url)

                # Add the extracted text to the data dictionary
                logger.info("Adding extracted text to the data dictionary.")
                data[title] = text

        return data


if __name__ == "__main__":

    # URL of the website
    sample_url = "https://www.defense.gov/news/"

    # Extract data from the website
    res = DataExtractor().extract_data(sample_url)

    print(res)
