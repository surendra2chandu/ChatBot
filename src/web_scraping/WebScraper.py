# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from src.conf.Configurations import logger


class WebScraper:


    def scraper(self, url):
        """
        This function scrapes the content of the specified URL and returns the target <div> element.
        :param url: The URL of the website to scrape.
        :return: The target <div> element if found, otherwise None.
        """

        # Fetch the content of the website
        logger.info(f"Fetching content from {url}")
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:

            # Successfully fetched content
            logger.info("Successfully fetched content.")

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the specific <div> with the class "alist-inner alist-more-here"
            target_div = soup.find('div', class_="alist-inner alist-more-here")

            if target_div:
                logger.info("Target <div> found.")
                return str(target_div)
            else:
                logger.warning("Target <div> not found on the page.")
                return None

    def get_content(self, url):
        """
        This function scrapes the content of the specified URL and returns the extracted text.
        :param url: The URL of the website to scrape.
        :return: The extracted text from <p> tags if found, otherwise None.
        """

        # Fetch the content of the website
        logger.info(f"Fetching content from {url}")
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Successfully fetched content
            logger.info("Successfully fetched content.")

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <p> tags on the page
            paragraphs = soup.find_all('p')

            # Extract text from each <p> tag
            all_paragraphs = [p.get_text(strip=True) for p in paragraphs]

            # Join paragraphs into a single string (optional, based on how you want the output)
            return "\n\n".join(all_paragraphs) if all_paragraphs else None
        else:
            logger.error(f"Failed to fetch content. Status code: {response.status_code}")
            return None



if __name__ == "__main__":

    # URL of the website
    sample_url1 = "https://www.defense.gov/news/"

    sample_url2 = "https://www.defense.gov/News/News-Stories/Article/Article/4037935/dod-orders-1500-troops-additional-assets-to-southern-border/"

    # Create an instance of the WebScraper class
    res = WebScraper().scraper(sample_url1)


    print(res)

    res = WebScraper().get_content(sample_url2)

    print(res)
