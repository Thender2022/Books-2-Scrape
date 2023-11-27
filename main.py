import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"
def scrape_product_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        #extracting single product
        product_page_url = url
        book_title = soup.h1.text.strip()
        upc_th = soup.find('th', string='UPC')
        upc = upc_th.find_next('td').text.strip()
        book_title = soup.h1.text.strip()
        price_including_tax = soup.find('th', text='Price (incl. tax)').find_next('td').string.strip()
        price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next('td').text.strip()
        quantity_available = soup.find('th', text='Availability').find_next('td').text.strip()
        product_description = soup.find('meta', {'name': 'description'})['content'].strip()
        category = soup.find('a', {'href': '../category/books/business_35/index.html'}).text.strip()
        review_rating = soup.find('th', text='Number of reviews').find_next('td').text.strip()
        image_url = soup.find('div', {'class': 'item active'}).img['src']


        print(f"Product Page URL: {product_page_url}")
        print(f"Book Title: {book_title}")
        print(f"UPC: {upc}")
        print(f"Price Including Tax: {price_including_tax}")
        print(f"Price Excluding Tax: {price_excluding_tax}")
        print(f"Quantity Available: {quantity_available}")
        print(f"Product Description: {product_description}")
        print(f"Category: {category}")
        print(f"Review Rating: {review_rating}")
        print(f"Image URL: {image_url}")

# URL of current Product
product_url = 'https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html'
scrape_product_page(product_url)


