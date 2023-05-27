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

# containers holding the links of the listing
urls = []

# Container holding listing name, price, and url
itemListing = []

# adding all links to their container
for links in resultsLinks:
    urls.append(links['href'])

counter = 0
len = len(results)
for x in resultsPrice:
    # Converts the price found from a string to a decimal float
    subString = x.text[1: 5]

    # Handles exception when subString is not able to be converted to decimal float
    try:
        filteredPrice = float(subString)
    except:
        pass

    # Filters price listings to only show those under $280
    if filteredPrice < 280:
        listingName = (results[counter].text + ' : ' + x.text + ' : ' + urls[counter])
        itemListing.append(listingName)
    if counter < len:
        counter += 1
