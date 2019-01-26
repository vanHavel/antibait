"""
This script scrapes unv.is urls for article titles and texts
"""

import logging
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from ftfy import fix_text

SCRAPED_DATA_DIR_PATH = Path('data', 'scraped')
URL_FILE_PATH = Path('data', 'urls.txt')


def scrape_unvis_urls() -> None:
    urls = read_urls_from_file(URL_FILE_PATH)
    for index, url in enumerate(urls):
        logger.info(f'Processing {url}...')
        page_content = get_html_content(url)
        title, text = extract_title_and_text(page_content)
        cleaned_text = clean_text(text)
        sample_filename = str(index) + '.txt'
        write_article_to_file(title, cleaned_text, url, sample_filename)


def read_urls_from_file(url_file_path: Path) -> List[str]:
    with url_file_path.open('r') as url_file:
        url_file_content = url_file.read()
    urls = url_file_content.split(sep='\n')
    return urls


def get_html_content(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def extract_title_and_text(page_content):
    html_doc = BeautifulSoup(page_content, 'html.parser')

    title_tag = html_doc.find('h1', class_='article-title')
    title = title_tag.get_text(separator=' ', strip=True)

    text_tag = html_doc.find_all('div', class_='container')[1] \
                       .find_all('div', class_='col-xs-12')[4] \
                       .find('div')
    text = text_tag.get_text(separator=' ', strip=True)

    return title, text


def clean_text(text: str) -> str:
    cleaned_text = fix_text(text)
    return cleaned_text


def write_article_to_file(title: str, text: str, url: str, filename: str) -> None:
    with (SCRAPED_DATA_DIR_PATH / filename).open('w') as article_file:
        lines_to_write = '\n'.join([url, title, text])
        article_file.write(lines_to_write)


if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    scrape_unvis_urls()

