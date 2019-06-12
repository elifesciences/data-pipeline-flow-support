import unittest
import json
from unittest.mock import  patch

from src import people_profile_json_download




class TestPeopleProfileJsonDownload(unittest.TestCase):

    def test_download_page_by_page(self):
        output_list=list()

        def append_to_list(json_row):
            json_row = json.loads(json_row)
            output_list.append(json_row)

        response = b"{\"total\": 2, \"items\": [{\"id\": \"testid1\", \"name\": {\"preferred\": \"name1 pref\", \"index\": \"name1 ,index\"}, \"orcid\": \"0005-0007-1754-3384\"}, {\"id\": \"id2\", \"name\": {\"preferred\": \"pref name2\", \"index\": \"name, index2\"}, \"orcid\": \"0340-0343-4760-8257\"}]}"
        with patch('urllib.request.urlopen', return_value=FakeResponse(data=response)) as mock_request:
            api_base_url_list = ['https://testurl.url']
            for api_base_url in api_base_url_list:
                output_list.clear()
                people_profile_json_download.download_page_by_page(api_base_url, output=append_to_list)

                self.assertTrue(len(output_list) == 2)
                print(len(output_list), output_list[0], type(output_list[1]))
                self.assertTrue('imported_timestamp' in output_list[0])
                self.assertTrue('id' in output_list[0])
                self.assertTrue('name' in output_list[0])


class FakeResponse:
    status: int
    data: bytes

    def __init__(self, *, data: bytes):
        self.data = data

    def read(self):
        self.status = 200 if self.data is not None else 404
        return self.data

    def close(self):
        pass


if __name__ == '__main__':
    unittest.main()



