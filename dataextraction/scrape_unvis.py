"""
This script scrapes unv.is urls for article titles and texts
"""

from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

RAW_DATA_DIR_PATH = Path('data', 'raw')
URL_FILE_PATH = Path('data', 'urls.txt')


def main() -> None:
    urls = read_urls_from_file(URL_FILE_PATH)
    for index, url in enumerate(urls):
        page_content = get_html_content(url)
        title, text = extract_title_and_text(page_content)
        sample_filename = str(index) + '.txt'
        write_article_to_file(title, text, url, sample_filename)


def read_urls_from_file(url_file_path: Path) -> List[str]:
    with url_file_path.open('r') as url_file:
        urls = url_file.readlines()
    return urls


def get_html_content(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def extract_title_and_text(page_content):
    html_doc = BeautifulSoup(page_content, 'html.parser')
    return "", ""


def write_article_to_file(title: str, text: str, url: str, filename: str) -> None:
    with (RAW_DATA_DIR_PATH / filename).open('w') as article_file:
        article_file.writelines([url, title, text])


if __name__ == '__main__':
    main()

