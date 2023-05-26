import requests
from bs4 import BeautifulSoup

# gets the webpage and creates a beautiful soup object to parse the web page 
url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=sony+xm5"&"_sacat=0'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# parses through html content to get listing name, link to listing, and price of listing
results = soup.find_all('div', class_='s-item__title')
resultsLinks = soup.find_all('a', class_="s-item__link")
resultsPrice = soup.find_all('span', class_='s-item__price')

# containers holding the links to the listings and their names
urls = []
listings = []

# adding all item names to their container
for listing in results:
    listings.append(listing.text)

# adding all links to their container
for links in resultsLinks:
    urls.append(links['href'])

counter = 0
for x in resultsPrice:
    # Converts the price found from a string to a decimal float
    # Need to find a way to handle exception when price found cannot be converted into float
    subString = x.text[1: 5]
    # Filters price listings to only show those under $280
    if float(subString) < 280:
        print(results[counter].text,":", x.text,":" , urls[counter])
    if counter < len(listings):
        counter += 1
