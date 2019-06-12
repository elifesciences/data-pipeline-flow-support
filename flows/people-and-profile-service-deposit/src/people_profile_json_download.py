"""
Primarily written to download data from the people and profile api of elifesciences
Writes the data primarily to stdout

@author: mowonibi
"""

import urllib.request, json, logging, sys, datetime
from datetime import timezone
from typing import Dict

# Create a custom logger
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)


def now():
    dtobj = datetime.datetime.now(timezone.utc)
    return dtobj.strftime("%Y-%m-%dT%H:%M:%SZ")


def download_data(data_url: str):
    """
    Tries to download data and covert downloaded data to json dictionary,
    if not possible return empty dict
    """
    print('redsds', data_url)
    try:
        response = urllib.request.urlopen(data_url)
        downloaded_data = response.read()
        downloaded_data = downloaded_data.decode('utf-8')
        try:
            downloaded_data = json.loads(downloaded_data, encoding='utf-8')
        except json.JSONDecodeError:
            logger.warning('data not decoded to json')
    except urllib.error.URLError:
        logger.warning('data not downloaded')
        downloaded_data = dict()

    return downloaded_data


def compose_url(api_base_url, url_param_dict: Dict[str, str]):
    """
    compose url from base api url and parameter dictionary

    """
    url_param = ''
    url_separator = '' if api_base_url.endswith('?') else '?'
    for key, value in url_param_dict.items():
        url_param += str(key) + '=' + str(value) +'&'
    return api_base_url + url_separator + url_param


def download_page_by_page(api_base_url, output=None, page_size=50):
    current_page = 1
    get_more_data = True
    out = output or print
    time_now = now()

    while get_more_data:
        data_page_url = compose_url(api_base_url, url_param_dict={'per-page': page_size, 'page': current_page})
        json_data = download_data(data_page_url)
        get_more_data = json_data.get('total', 1) > page_size * current_page

        for row in json_data.get('items', []):
            row["imported_timestamp"] = time_now
            out(json.dumps(row))

        current_page += 1


if __name__ == '__main__' :
    args = sys.argv[1:]
    root_profile_url = args[0]

    try:
        page_size = int(args[1])
        page_size = 100 if page_size > 100 else page_size
    except IndexError:
        page_size = 100

    download_page_by_page(root_profile_url, page_size=page_size)

