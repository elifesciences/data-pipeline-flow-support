import unittest
import json
from unittest.mock import patch

from src import people_profile_json_download
from unittest.mock import MagicMock


class TestPeopleProfileJsonDownload(unittest.TestCase):
    def test_download_page_by_page(self):
        output_list = list()
        time_now = people_profile_json_download.now()
        response = b'{"total": 2, "items": [{"id": "testid1", "name": {"preferred": "name1 pref", "index": "name1, index"}, "orcid": "0005-0007-1754-3384"}, {"id": "id2", "name": {"preferred": "pref name2", "index": "name, index2"}, "orcid": "0340-0343-4760-8257"}]}'

        def append_to_list(json_row):
            json_row = json.loads(json_row)
            output_list.append(json_row)

        with patch("urllib.request.urlopen") as mock_urlopen:
            response_mock = MagicMock()
            response_mock.read.return_value = response
            mock_urlopen.return_value = response_mock
            api_base_url_list = ["https://testurl.url"]
            for api_base_url in api_base_url_list:
                output_list.clear()
                people_profile_json_download.download_page_by_page(
                    api_base_url, time_now=time_now, output=append_to_list
                )
                self.assertTrue(len(output_list) == 2)
                self.assertTrue("imported_timestamp" in output_list[0])
                self.assertTrue("id" in output_list[0])
                self.assertTrue("name" in output_list[0])
                self.assertTrue(output_list[0].get("id") == "testid1")
                self.assertTrue(output_list[0].get("imported_timestamp") == time_now)
                self.assertTrue(
                    output_list[0].get("name").get("preferred") == "name1 pref"
                )
                self.assertTrue(
                    output_list[0].get("name").get("index") == "name1, index"
                )
                self.assertTrue(output_list[0].get("orcid") == "0005-0007-1754-3384")


if __name__ == "__main__":
    unittest.main()
