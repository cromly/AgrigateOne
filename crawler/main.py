# AgrigateOne Assignment for Louis Bouwer
# Using JetBrains PyCharm 2022.2.1
# Press Shift+F10 to execute.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# This Python script defines functions for getting links from a webpage (get_links) and
# for downloading a webpage (download_page).
# The crawl function uses a breadth-first search approach to crawl up to max_pages number of pages
# starting from start_url.
# It utilizes multiprocessing with up to processes parallel processes.

# Function to recursively explore links at a given depth
# A nested function explore_links to recursively explore links at a given depth.
# Inside explore_links, the HTML content of the current URL are being fetched and extract links.
# If the maximum pages retrieved limit has not been reached,
# increment the depth and recursively explore links at the next depth level.
# Call explore_links initially with the initial URL and depth 0.
# This approach ensures that the function continue exploring links at deeper levels until it retrieve
# the desired number of pages specified by max_pages.

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool


def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)


def fetch_html_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Failed to fetch HTML content from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: Failed to fetch HTML content from {url}. Exception: {e}")
        return None


def get_links(url, max_pages):
    print("Starting get_links function...")

    links = []
    visited = set()
    pages_retrieved = 0
    depth = 0

    def explore_links(current_url, current_depth):
        nonlocal pages_retrieved, links, visited, depth
        html_content = fetch_html_content(current_url)
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(current_url, link['href'])
            if is_valid_url(absolute_url) and absolute_url not in visited:
                links.append((absolute_url, current_depth + 1))
                visited.add(absolute_url)
                pages_retrieved += 1

                if pages_retrieved >= max_pages:
                    return

    explore_links(url, depth)

    while pages_retrieved < max_pages and links:
        url, depth = links.pop(0)
        explore_links(url, depth)

    print("Finished get_links function.")
    return links


def download_page(url, folder):
    print(f"Downloading page: {url}")
    response = requests.get(url)
    filename = os.path.join(folder, f"{url.split('/')[-1]}.html")
    with open(filename, 'wb') as f:
        f.write(response.content)


def clean_directory(folder):
    print("Cleaning directory...")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    print("Directory cleaned.")


def crawl(start_url, max_pages, processes):
    print("Starting crawl function...")
    folder = '../pages'
    os.makedirs(folder, exist_ok=True)
    clean_directory(folder)

    links = get_links(start_url, max_pages)
    visited = set()

    downloaded_pages = 0

    with Pool(processes) as pool:
        while downloaded_pages < max_pages and links:
            url, _ = links.pop(0)
            if url in visited:
                continue
            visited.add(url)
            print(f"Downloading: {url}")
            pool.apply_async(download_page(url, folder), (url, folder))
            downloaded_pages += 1

        pool.close()
        pool.join()

    print("Finished crawl function.")


if __name__ == "__main__":
    start_url = 'https://bikehub.co.za/classifieds/g/bikes'
    max_pages = 10
    processes = 2
    crawl(start_url, max_pages, processes)
