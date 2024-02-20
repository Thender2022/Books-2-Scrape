import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_site(base_url):
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the category links
        category_links = soup.find_all('a', href=lambda href: href and 'catalogue/category/books' in href)

        for category_link in category_links:
            relative_url = category_link['href']
            category_url = urljoin(base_url, relative_url)
            print("Category URL:", category_url)

            scrape_category_books(category_url)

def scrape_category_books(category_url):
    response = requests.get(category_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the links to books in the current category
        book_links = soup.find_all('h3')

        for book_link in book_links:
            relative_url = book_link.a['href']
            book_url = urljoin(category_url, relative_url)
            print("Book URL:", book_url)

            scrape_book_details(book_url)

def scrape_book_details(book_url):
    response = requests.get(book_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        #  Extract book information from the current book page
        book_title = soup.h1.text.strip()
        book_script = soup.find('div', class_='sub-header')
        book_description = book_script.find_next('p').text.strip()
        tbody_elements = soup.table.find_all('tr')
        tbody_list = list(tbody_elements)
        upc = tbody_list[0].td.text.strip()
        price_w_tax = tbody_list[2].td.text.strip()
        price_no_tax = tbody_list[3].td.text.strip()
        avail = tbody_list[5].td.text.strip()
        rating_tag = soup.find('p', class_="star-rating")
        rating = rating_tag['class'][1]
        img_url = urljoin(book_url, soup.img['src'])

        print(f"Book Title: {book_title}")
        print(f"Book Description: {book_description}")
        print(f"UPC: {upc}")
        print(f"Price (incl. tax): {price_w_tax}")
        print(f"Price (excl. tax): {price_no_tax}")
        print(f"Availability: {avail}")
        print(f"Star Rating: {rating}")
        print(f"Image URL: {img_url}")
        print("\n")

base_url = 'https://books.toscrape.com/index.html'
scrape_site(base_url)


# def scrape_site(base_url):
#     response = requests.get(base_url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         articles = soup.find_all('article', class_='product_pod')
#         for article in articles:
#             book_title = article.h3.a['title']
#             book_url = article.h3.a['href']
#
#             print(f'Title: {book_title}')
#             print(f'URL: {base_url}/{book_url}\n')
#
# base_url = 'https://books.toscrape.com/index.html'
# scrape_site(base_url)

# ----------------

# def scrape_catalog(catalog_url):
#     response = requests.get(catalog_url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         category_list = soup.find_all('ul', class_="nav-list")
#
#         for category in category_list:
#             # Find the anchor tag within the ul element
#             anchor_tags = category.find_all('a')
#
#             for anchor_tag in anchor_tags:
#                 relative_url = anchor_tag.get('href')
#                 # Construct the full URL using urljoin
#                 category_url = urljoin(catalog_url, relative_url)
#                 print("Book Category URL:", category_url, "\n")
#
#                 scrape_books(category_url)
#
# def scrape_books(category_url):
#     response = requests.get(category_url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Modify the following code to extract book information from the current category page
#         book_titles = soup.find_all('h3')  # Adjust based on the actual structure
#         for title in book_titles:
#             print("Book Title:", title.text.strip())
#
#
# catalog_url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
# scrape_catalog(catalog_url)

# -----------------------

# def scrape_site(base_url):
#     for i in range(1, 51):
#         site_url = f'{base_url}/page-{i}.html'
#         response = requests.get(site_url)
#
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             # nav_list = soup.find('ul', class_='nav-list')
#             #
#             # if nav_list:
#             #     # Extract all category links from the navigation list
#             #     category_links = nav_list.find_all('a')
#             #
#             #     # Extract category names from the links
#             #     categories = [link.text.strip() for link in category_links]
#             #
#             #     # Print the list of categories
#             #     # print(category_links)
#             #     for category in categories:
#             #         print(category)
#
#  # used to get all books of category
#             article_containers = soup.find_all('ol')
#             for article_container in article_containers:
#                 articles = article_container.find_all('article', class_='product_pod')
#
#                 for article in articles:
#                     category_name = article.select_one('div.image_container img')['alt']
#
#                     book_title = article.h3.a['title']
#                     book_url = article.h3.a['href']
#
#                     print(f'Title: {book_title}')
#                     print(f'URL: {book_url}\n')
#                     # print(f'{category_name}\n')  # Print category for each book
#
# base_url = 'https://books.toscrape.com/catalogue'
# scrape_site(base_url)



# _______________


# def scrape_catalog_page(catalog_url):
#     response = requests.get(catalog_url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         categories = []
#         catalog_page_url = catalog_url
#         category_containers = soup.find_all('ul', class_='nav-list')
#
#         for ul in category_containers:
#             categories = ul.find_all('li')
#
#             for category in categories:
#                 category_title = category.a.text.strip()
#                 print(f"Category Title: {category_title}")

# class Book:
#     def __init__(self, upc, product_title, price_including_tax, price_excluding_tax, quantity_available,
#                  product_description, category, review_rating, image_url):
#         self.upc = upc
#         self.product_title = product_title
#         self.price_including_tax = price_including_tax
#         self.price_excluding_tax = price_excluding_tax
#         self.quantity_available = quantity_available
#         self.product_description = product_description
#         self.category = category
#         self.review_rating = review_rating
#         self.image_url = image_url
#
# def scrape_category(category_url):
#     response = requests.get(category_url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         category_containers = soup.find_all('article', class_='product_pod')
#
#         books_data = []
#
#         for container in category_containers:
#             relative_product_url = container.a['href']
#             full_product_url = urljoin(category_url, relative_product_url)
#
#             book_data = scrape_product_info(full_product_url)
#             books_data.append(book_data)
#
#             # Writing all book info to csv
#             csv_filename = 'category.csv'
#             with open(csv_filename, 'w', newline='') as csvfile:
#                 fieldnames = ['upc', 'book_title', 'price_including_tax',
#                               'price_excluding_tax', 'quantity_available', 'product_description',
#                               'category', 'review_rating', 'image_url']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 for book in books_data:
#                     writer.writerow({
#                         'upc': book.upc,
#                         'book_title': book.product_title,
#                         'price_including_tax': book.price_including_tax,
#                         'price_excluding_tax': book.price_excluding_tax,
#                         'quantity_available': book.quantity_available,
#                         'product_description': book.product_description,
#                         'category': book.category,
#                         'review_rating': book.review_rating,
#                         'image_url': book.image_url
#                     })
#
#             print("{csv_filename}")
# def scrape_product_info(full_product_url):
#     response = requests.get(full_product_url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         upc_th = soup.find('th', string='UPC')
#         upc = upc_th.find_next('td').text.strip()
#         product_title = soup.h1.text.strip()
#         price_including_tax = soup.find('th', string='Price (incl. tax)').find_next('td').string.strip()
#         price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text.strip()
#         quantity_available = soup.find('th', string='Availability').find_next('td').text.strip()
#         ul_element = soup.find('ul')
#         list_items = ul_element.find_all('li')
#         category = list_items[2].text.strip()
#         review_rating = soup.find('th', string='Number of reviews').find_next('td').text.strip()
#         image_url = soup.find('div', {'class': 'item active'}).img['src']
#         product_description = soup.find('meta', {'name': 'description'})['content'].strip()
#
#         return Book(upc, product_title, price_including_tax, price_excluding_tax, quantity_available,
#                     product_description, category, review_rating, image_url)
# #
# # # Example usage
# #
# # catalog_url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
# # scrape_catalog_page(catalog_url)
# # # scrape_books_in_category(catalog_url)
# category_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'
# scrape_category(category_url)


