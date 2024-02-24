import os
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

        # Create a main folder for the entire scraping session
        main_folder = os.path.join(os.getcwd(), 'scraped_data')
        os.makedirs(main_folder, exist_ok=True)

        for category_link in category_links[1:]:  # Skip the first link as it's usually a non-category link
            category_name = category_link.text.strip()
            relative_url = category_link['href']
            category_url = urljoin(base_url, relative_url)
            category_folder = create_category_folder(category_name, main_folder)
            print("Category URL:", category_url)

            scrape_category_books(category_url, category_folder)

def create_category_folder(category_name, main_folder):
    base_path = os.path.join(main_folder, 'categories')
    category_folder = os.path.join(base_path, category_name)
    os.makedirs(category_folder, exist_ok=True)
    return category_folder

def scrape_category_books(category_url, category_folder):
    while category_url:
        response = requests.get(category_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the links to books in the current category
            book_links = soup.find_all('h3')

            for book_link in book_links:
                relative_url = book_link.a['href']
                book_url = urljoin(category_url, relative_url)
                print("Book URL:", book_url)

                book_data = scrape_book_details(book_url, category_folder)
                if book_data:
                    write_to_csv(book_data, category_folder)

            next_button = soup.select_one('li.next > a')
            if next_button:
                category_url = urljoin(category_url, next_button['href'])
            else:
                category_url = None
        else:
            print("Failed to retrieve category page")
            category_url = None

def scrape_book_details(book_url, category_folder):
    response = requests.get(book_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract book information
        book_title = soup.h1.text.strip()
        book_description = soup.select_one('meta[name="description"]')['content'].strip()
        product_table = {row.th.text.strip(): row.td.text.strip() for row in soup.select('table.table.table-striped tr')}
        upc = product_table.get('UPC')
        price_incl_tax = product_table.get('Price (incl. tax)')
        price_excl_tax = product_table.get('Price (excl. tax)')
        availability = product_table.get('Availability')
        rating = soup.find('p', class_='star-rating')['class'][1]
        image_url = urljoin(book_url, soup.find('img')['src'])

        image_filename = f'{book_title}.jpg'
        image_path = os.path.join(category_folder, 'images', image_filename)
        download_image(image_url, image_path)

        return {
            "Title": book_title,
            "Description": book_description,
            "UPC": upc,
            "Price (incl. tax)": price_incl_tax,
            "Price (excl. tax)": price_excl_tax,
            "Availability": availability,
            "Rating": rating,
            "Image URL": image_path,
        }

def write_to_csv(book_data, category_folder):
    csv_file_path = os.path.join(category_folder, 'books_data.csv')
    file_exists = os.path.isfile(csv_file_path)

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = list(book_data.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(book_data)

def download_image(image_url, image_path):
    response = requests.get(image_url)

    if response.status_code == 200:
        # Create an 'images' folder within the category folder
        images_folder = os.path.join(os.path.dirname(image_path), 'images')
        os.makedirs(images_folder, exist_ok=True)

        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
    else:
        print(f"Failed to download image from {image_url}")

base_url = 'https://books.toscrape.com/index.html'
scrape_site(base_url)


