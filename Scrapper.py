import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to scrape Amazon website
def scrape_amazon(url, website_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
        }

        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, 'html.parser')

        product_name = soup.find('span', 'a-size-large product-title-word-break').text
        price_parent = soup.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text

        return website_name, product_name, price
    except Exception as e:
        return website_name, '', ''

# Function to scrape Flipkart website
def scrape_flipkart(url, website_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
        }

        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, 'html.parser')

        product_name = soup.find('span', 'B_NuCI').text
        price = soup.find('div', '_30jeq3 _16Jk6d').text

        return website_name, product_name, price
    except Exception as e:
        return website_name, '', ''

# Function to convert price string to numeric value
def convert_to_numeric(price_string):
    try:
        price_numeric = float(price_string.replace('₹', '').replace(',', ''))
        return price_numeric
    except ValueError:
        return 0.0  

amazon_scraping_successful = False
flipkart_scraping_successful = False

# Scrape Amazon website
print("Please enter the link from Amazon")
url = input()
for _ in range(50):
    amazon_data = scrape_amazon(url, 'Amazon')

    if amazon_data[1]:
        amazon_scraping_successful = True
        break

# Scrape Flipkart website
print("Please enter the link from Flipkart")
flipkart_url = input()
for _ in range(5):
    flipkart_data = scrape_flipkart(flipkart_url, 'Flipkart')

    if flipkart_data[1]:
        flipkart_scraping_successful = True
        break

# Process scraped data if successful scraping occurred on both websites
if amazon_scraping_successful and flipkart_scraping_successful:
    price_amazon_numeric = convert_to_numeric(amazon_data[2])
    price_flipkart_numeric = convert_to_numeric(flipkart_data[2])

    price_difference = abs(price_amazon_numeric - price_flipkart_numeric)

    # Prepare data for CSV
    data = {
        'Website': [amazon_data[0], flipkart_data[0], 'Price Difference'],
        'Product Name': [amazon_data[1], flipkart_data[1], ''],
        'Price': [amazon_data[2], flipkart_data[2], price_difference]
    }

    if price_amazon_numeric < price_flipkart_numeric:
        data['Product Name'][2] = 'Price in Amazon is Cheaper by flipkart'
    elif price_amazon_numeric > price_flipkart_numeric:
        data['Product Name'][2] = 'Price in Flipkart is Cheaper by amazon'
    else:
        data['Product Name'][2] = 'Prices are the Same'
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    # Create DataFrame and save to CSV
    filename = input("Enter the filename: ")
    df = pd.DataFrame(data)
    df.to_csv(filename + '.csv', index=False)
else:
    print("Scraping was unsuccessful for one or both websites.")