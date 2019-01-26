"""
This script scrapes unv.is urls for article titles and texts
"""
from pathlib import Path

RAW_DATA_DIR_PATH = Path('data', 'raw')
URL_FILE_PATH = Path('data', 'urls.txt')


def write_article_to_file(title: str, text: str, url: str, filename: str) -> None:
    with (RAW_DATA_DIR_PATH / filename).open('w') as article_file:
        article_file.writelines([url, title, text])


if __name__ == '__main__':
    urls = read_urls_from_file(URL_FILE_PATH)
    for index, url in enumerate(urls):
        page_content = get_content(url)
        title, text = extract_title_and_text(page_content)
