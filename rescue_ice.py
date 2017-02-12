import requests
import bs4
import urllib
import os
import logging

logging.basicConfig(level=logging.INFO)


def getNextPage(listingUrl):
    logging.info(('Going to page %s') % (listingUrl.split('=')[-1]))
    response = requests.get(listingUrl);
    soup = bs4.BeautifulSoup(response.text, 'html.parser');
    return {
        'soup': soup,
        'nextPage': soup.select_one('.pages .current + li')
    }


def getProducts(soup):
    links = []
    for link in soup.select('.item .product-image'):
        links.append(link['href'])
    return links


def getAkki(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    productName = soup.select_one('.product-main-info .product-name h1').get_text()
    productColor = soup.select_one('.color-swatch .attribute-label span').get_text()
    productUniqueName = url.split('/')[-1]

    try:
        logging.info(('Creating folder for %s - %s' % (productName, productColor)))
        os.makedirs(productUniqueName)
    except OSError:
        if not os.path.isdir(productUniqueName):
            raise

    for i, akki in enumerate(soup.select('.main-image-set img')):
        logging.info(('Saving image %s of %s') % (i + 1, len(soup.select('.main-image-set img'))))
        urllib.urlretrieve(akki['data-zoom-image'], '%s/%s.jpg' % (productUniqueName, i))


def rescueIce():
    listingUrl = 'http://www.icedesign.com.au/clothing';

    def rescueAkkis(url):
        pageData = getNextPage(url)
        for product in getProducts(pageData['soup']):
            getAkki(product)

        try:
            rescueAkkis(pageData['nextPage'].a['href'])
        except AttributeError:
            print "Thats all folks...!"

    rescueAkkis(listingUrl)


rescueIce()
