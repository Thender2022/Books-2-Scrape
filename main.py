import requests
import csv
from bs4 import BeautifulSoup

# def scrape_product_page(url):
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         #extracting single product
#         product_page_url = url
#         book_title = soup.h1.text.strip()
#         product_description = soup.find('meta', {'name': 'description'})['content'].strip()
#         upc_th = soup.find('th', string='UPC')
#         upc = upc_th.find_next('td').text.strip()
#         price_including_tax = soup.find('th', text='Price (incl. tax)').find_next('td').string.strip()
#         price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next('td').text.strip()
#         quantity_available = soup.find('th', text='Availability').find_next('td').text.strip()
#         category = soup.find('a', {'href': '../category/books/business_35/index.html'}).text.strip()
#         review_rating = soup.find('th', text='Number of reviews').find_next('td').text.strip()
#         image_url = soup.find('div', {'class': 'item active'}).img['src']
#
#         # Writing single book info to csv
#         csv_filename = 'book_data.csv'
#         with open(csv_filename, 'w', newline='') as csvfile:
#             fieldnames = ['product_page_url', 'upc', 'book_title', 'price_including_tax',
#                           'price_excluding_tax', 'quantity_available', 'product_description',
#                           'category', 'review_rating', 'image_url']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#             writer.writeheader()
#
#             writer.writerow({
#                 'product_page_url': product_page_url,
#                 'upc': upc,
#                 'book_title': book_title,
#                 'price_including_tax': price_including_tax,
#                 'price_excluding_tax': price_excluding_tax,
#                 'quantity_available': quantity_available,
#                 'product_description': product_description,
#                 'category': category,
#                 'review_rating': review_rating,
#                 'image_url': image_url
#             })
#
#             print(f"Data written to {csv_filename}")
#
#         print(f"Product Page URL: {product_page_url}")
#         print(f"Book Title: {book_title}")
#         print(f"Product Description: {product_description}")
#         print(f"UPC: {upc}")
#         print(f"Price Including Tax: {price_including_tax}")
#         print(f"Price Excluding Tax: {price_excluding_tax}")
#         print(f"Quantity Available: {quantity_available}")
#         print(f"Category: {category}")
#         print(f"Review Rating: {review_rating}")
#         print(f"Image URL: {image_url}")


def scrape_category_page(category_url):
    response = requests.get(category_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

#     Extracting Category Page
        category_page_url = category_url
        book_containers = soup.find_all('article', class_='product_pod')

        print(f"Category Page URL: {category_page_url}")
        print("Book Information:")

# Extracting from book title from the h3 tag within article
        for book in book_containers:
            book_title = book.h3.a['title']

            product_page_url = book.h3.a['href']

            product_page_url = f'https://books.toscrape.com/catalogue{product_page_url}'
            product_info = scrape_product_page(product_page_url)

            # Print or process the extracted information as needed
            print(f"Book Title: {book_title}")
            print(f"Product Page URL: {product_page_url}")
            print("Additional Information:")
            print(product_info)
            print("\n")

def scrape_product_page(product_url):
    response = requests.get(product_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract additional information from the product page
        book_info = {
            'book_title': soup.h1.text.strip(),
            'product_description': soup.find('meta', {'name': 'description'})['content'].strip(),
            'upc': soup.find('th', string='UPC').find_next('td').text.strip(),
            'price_including_tax': soup.find('th', text='Price (incl. tax)').find_next('td').string.strip(),
            'price_excluding_tax': soup.find('th', text='Price (excl. tax)').find_next('td').text.strip(),
            'quantity_available': soup.find('th', text='Availability').find_next('td').text.strip(),
            'category': soup.select_one('ul.breadcrumb > li:nth-child(3) > a').text.strip(),
            # 'category': soup.find('a', {'href': '../../../category/books/business_35/index.html'}).text.strip(),
            'review_rating': soup.find('th', text='Number of reviews').find_next('td').text.strip(),
            'image_url': soup.find('div', {'class': 'item active'}).img['src'],
        }

        return book_info



# URL of current Product
# product_url = 'https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html'
category_url = 'https://books.toscrape.com/catalogue/category/books/business_35/index.html'
# scrape_product_page(product_url)
scrape_category_page(category_url)



# Site URL
# site_url = 'https://books.toscrape.com/index.html'


