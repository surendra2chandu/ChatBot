from bs4 import BeautifulSoup
import requests

html_content = """<div class="alist-inner alist-more-here">
<feature-template :remove-grid="true" :show-all="true" template-mode="story">
<listing-with-preview :show-image="true" article-alt="Social media image for the Department of Defense website." article-id="4016173" article-image-url="" article-summary="Today's Defense Department contracts valued at $7.5 million or more are now live on Defense.gov." article-title="Contracts for Dec. 23, 2024" article-url="https://www.defense.gov/News/Contracts/Contract/Article/4016173//" article-url-or-link="https://www.defense.gov/News/Contracts/Contract/Article/4016173//" article-url-or-link-absolute="https://www.defense.gov/News/Contracts/Contract/Article/4016173//" category="" content-type-name="Contracts" content-type-val="400" image-caption="Social media image for the Department of Defense website." image-url="https://media.defense.gov/2021/Sep/30/2002865211/825/780/0/210930-D-EX074-013.JPG" item-index="1" open-in-new="" publish-date-ap="Dec. 23, 2024" publish-date-jss="2024-12-23T17:00:31" term-name="" term-url="">
</listing-with-preview>
</feature-template>
</div>"""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser' )

# Find all listing elements
listings = soup.find_all('listing-with-preview')

# Extract data
for listing in listings:
    content_type = listing.get('content-type-name', 'Unknown').strip()
    publish_date = listing.get('publish-date-ap', 'Unknown').strip()
    title = listing.get('article-title', 'Unknown').strip()
    summary = listing.get('article-summary', 'Unknown').strip()
    artical_url = listing.get('article-url', 'Unknown').strip()

    # print(f"{content_type} | {publish_date}")
    # print(f"{title}")
    # print(f"{summary}")
    # print(f"{artical_url}")


    # Fetch the content of the website
    response = requests.get(artical_url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specific <div> with the class "alist-inner alist-more-here"
        target_div = soup.find('div', class_="body")

        print( target_div.text)
    print()