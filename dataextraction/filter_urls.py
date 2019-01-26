"""
This script filters urls extracted from reddit and converts them to unv.is urls if necessary
"""

from pathlib import Path

INPUT_URL_FILE_PATH = Path('data', 'reddit_urls.txt')
OUTPUT_URL_FILE_PATH = Path('data', 'unvis_urls.txt')
ALLOWED_HOSTS = [
    'unv.is',
    'thesun.co.uk',
    'iflscience.com',
    'cnbc.com',
    'independent.co.uk',
    'bbc.com',
    'digitalspy.com',
    'cnn.com',
    'dailymail.co.uk',
    'businessinsider.com'
]

if __name__ == '__main__':
    with INPUT_URL_FILE_PATH.open('r') as input_file:
        urls = input_file.read().split('\n')
    filtered_urls = [url for url in urls if any([host in url for host in ALLOWED_HOSTS])]
    extended_urls = [f'https://unv.is/{url}' if 'unv.is' not in url else url for url in filtered_urls]
    with OUTPUT_URL_FILE_PATH.open('w') as output_file:
        output_file.write('\n'.join(extended_urls))
