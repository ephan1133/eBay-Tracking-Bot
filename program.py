import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import ssl
import smtplib
import time
from datetime import datetime
import pytz

while(True):
    # gets the webpage and creates a beautiful soup object to parse the web page 
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=sony+xm5"&"_sacat=0'
    itemName = 'Sony XM5'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # parses through html content to get listing name, link to listing, and price of listing
    results = []
    resultsLinks = []
    resultsPrice = []
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
    length = len(results)
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
        if counter < length:
            counter += 1

    # this part of the code handles sending the user an email when there are eligible items

    # EDIT THIS LINE IF USER WANTS TO CHANGE EMAIL DESTINATION
    destination = 'ephan6961@gmail.com'
    # sender of email
    sender = 'eppythonbotemail@gmail.com'

    # instantiating EmailMessage object
    email = EmailMessage()
    # 16 digit app password to email
    emailPassword = 'sfbfclbvpyfquymb'
    # setting email to send from
    email['From'] = sender
    # setting the email to send to
    email['To'] = destination
    # setting subject of the email
    email['Subject'] = 'Here are the price listings currently for: ' + itemName
    # creates the body of the email
    NY_time_zone = pytz.timezone('America/New_York')
    NY_time = datetime.now(NY_time_zone)
    current_time = NY_time.strftime("%I:%M:%S %p")

    body = "At time: " + current_time + "\n \n"
    for item in itemListing:
        body += item + "\n  \n"
    # setting the body of the email from created body message
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, emailPassword)
        smtp.sendmail(sender, destination, email.as_string())

    length = 0
    time.sleep(3600)