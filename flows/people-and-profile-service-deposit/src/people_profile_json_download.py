"""
Primarily written to download data from the people and profile api of elifesciences
Writes the data primarily to stdout

@author: mowonibi
"""

from urllib import request, parse, error
import json
import sys
import datetime
from datetime import timezone


def now():
    dtobj = datetime.datetime.now(timezone.utc)
    return dtobj.strftime("%Y-%m-%dT%H:%M:%SZ")


def download_data(data_url: str):
    """
    Tries to download data and covert downloaded data to json dictionary,
    if not possible return empty dict
    """
    try:
        response = request.urlopen(data_url)
        downloaded_data = response.read()
        downloaded_data = downloaded_data.decode("utf-8")
        try:
            downloaded_data = json.loads(downloaded_data, encoding="utf-8")
        except json.JSONDecodeError:
            sys.stderr.write("data in %s not decoded to json" % data_url)
    except error.URLError:
        sys.stderr.write("data in %s not downloaded" % data_url)
        downloaded_data = dict()

    return downloaded_data


def download_page_by_page(api_base_url, time_now, output=None, page_size=50):
    """
    Download all data page by page from api_base_url
    """
    current_page = 1
    get_more_data = True
    out = output or print

    while get_more_data:
        # create url
        url_separator = "" if api_base_url.endswith("?") else "?"
        url_param_dict = {"per-page": page_size, "page": current_page}
        params = "&".join(
            ["%s=%s" % (k, parse.quote(str(v))) for k, v in url_param_dict.items()]
        )
        data_page_url = api_base_url + url_separator + params
        # download data
        json_data = download_data(data_page_url)
        get_more_data = json_data.get("total", 0) > page_size * current_page

        for row in json_data.get("items", []):
            row["imported_timestamp"] = time_now
            out(json.dumps(row))

        current_page += 1


if __name__ == "__main__":
    ARGS = sys.argv[1:]
    ROOT_PROFILE_URL = ARGS[0]
    try:
        PAGE_SIZE = int(ARGS[1])
        PAGE_SIZE = 100 if PAGE_SIZE > 100 else PAGE_SIZE
    except IndexError:
        PAGE_SIZE = 100

    download_page_by_page(ROOT_PROFILE_URL, time_now=now(), page_size=PAGE_SIZE)
