"""
This python script scrapes the "Saved you a click" subreddit for unvis urls
"""

import logging
import requests
import time
from pathlib import Path
from typing import Any, Dict, List,Set

URL_FILE_PATH = Path('data', 'reddit_urls.txt')
SUBREDDIT_NAME = 'savedyouaclick'


def scrape_urls_from_reddit() -> None:
    all_urls = get_submission_urls(SUBREDDIT_NAME)
    url_lines = '\n'.join(all_urls)
    with URL_FILE_PATH.open('w') as url_file:
        url_file.write(url_lines)


def get_submission_urls(subreddit_name: str) -> Set[str]:
    query_before_time = int(time.time())
    urls = set()
    done = False
    while not done:
        results = pushshift_request(subreddit_name, query_before_time)
        logger.info(f'Queried {len(results)} submissions before {query_before_time}')
        if len(results) == 0:
            done = True
        else:
            query_before_time = min([submission['created_utc'] for submission in results])
            urls |= {submission['url'] for submission in results}
    return urls


def pushshift_request(subreddit_name: str, query_before_time: int) -> List[Dict[str, Any]]:
    url = 'https://api.pushshift.io/reddit/search/submission/'
    params = {'subreddit': subreddit_name, 'size': 500, 'before': query_before_time}
    response = requests.get(url, params=params)
    return response.json()['data']


if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    scrape_urls_from_reddit()
