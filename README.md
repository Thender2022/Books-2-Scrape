OpenClassrooms Python Bootcamp Project #2

Books2Scrape

I created this ETL pipeline To simplify the processes and tools used to extract, transform, and load data. In this case we scraped information from [Books2Scrape](books.toscrape.com) and by doing this I was able to scrape all of the books from the website and categorize them in CSV files that should be easy navigate.

The project was built with Python using an IDE called PyCharm.

There were also 5 other components that played a major role in the functionality of this project and they are explained in the following:

1. import os; 
- This module provides a way of interacting with the operating system. Allowing me to use functionalities like manipulating paths. You can see this being used on line 17 in the main.py file, this is allowing me to create a folder for ALL scraped data and then a separate folder for each category of books.
2. import requests;
- This is a third-party library for sending HTTP requests and handling responses
3. BeautifulSoup(bs4);
- Third party library used for web scraping that allows you to extract data from HTML and XML files by providing pythonic idioms for iterating, searching, and modifying the parse tree.
4. from urllib.parse import urljoin;
- urllib.parse is a module that provides functions for parsing URLs. In this case it was used for joining base URLs with relative URLs. This you can see being used on line 47 in the main.py file to connect the category pages so that all books on every page could be scraped.
