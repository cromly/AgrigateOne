# AgrigateOne Assignment for Louis Bouwer
# Using JetBrains PyCharm 2022.2.1
# Press Shift+F10 to execute.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# This script defines functions for getting links from a webpage (get_links) and
# for downloading a webpage (download_page).
# The crawl function uses a breadth-first search approach to crawl up to max_pages number of pages
# starting from start_url.
# It utilizes multiprocessing with up to processes parallel processes.


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Pool


def get_links(url, max_depth, max_pages):
    print("---- Get Links ------")
    links = []  # Use a list to store links and their depths
    visited = set()  # Track visited URLs to avoid revisiting
    queue = [(url, 0)]  # Initialize queue with the starting URL and depth 0
    pages_retrieved = 0  # Counter for retrieved pages

    while queue:
        if pages_retrieved >= max_pages:
            break  # Stop retrieving pages if max_pages limit is reached

        current_url, depth = queue.pop(0)
        if depth > max_depth:
            continue  # Skip if depth exceeds max_depth

        if current_url not in visited:
            visited.add(current_url)
            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(current_url, link['href'])
                    links.append((absolute_url, depth))  # Include depth with the link
                    if depth + 1 <= max_depth:
                        queue.append((absolute_url, depth + 1))
                pages_retrieved += 1  # Increment retrieved pages counter
            except Exception as e:
                print(f"Error scraping {current_url}: {e}")

    return links


def download_page(url, folder):
    print("------- Start download_page")
    response = requests.get(url)
    filename = os.path.join(folder, f"{url.split('/')[-1]}.html")
    with open(filename, 'wb') as f:
        f.write(response.content)


def clean_directory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def crawl(start_url, max_pages, max_depth, processes):
    folder = 'pages'
    os.makedirs(folder, exist_ok=True)

    # Clean the directory before starting crawling
    clean_directory(folder)

    # Scrape links from the initial URL
    links = get_links(start_url, max_depth, max_pages)
    visited = set()  # Initialize set to track visited links

    downloaded_pages = 0  # Counter for downloaded pages

    with Pool(processes) as pool:
        while downloaded_pages < max_pages and links:
            url, _ = links.pop(0)
            if url in visited:
                continue  # Skip if URL has already been visited
            visited.add(url)  # Mark URL as visited

            print(f"Downloading: {url}")
            pool.apply_async(download_page, (url, folder,))
            downloaded_pages += 1  # Increment downloaded pages counter

        # Close the pool to prevent any more tasks from being submitted
        pool.close()
        # Wait for all the worker processes to complete
        pool.join()

if __name__ == "__main__":
    start_url = 'https://webscraper.io/test-sites/e-commerce/allinone'
    max_pages = 10
    max_depth = 1
    processes = 2
    crawl(start_url, max_pages, max_depth, processes)
