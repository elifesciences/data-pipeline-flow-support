import unittest
from io import StringIO
import json

from src import reviewercsv2bq


class TestReviewersCsv2Bq(unittest.TestCase):

    def test_process_file_stream_content(self):
        self.maxDiff=None
        test_text = "\"1\",\"2\",\"3\",\"4\",\"5\"\n"\
                    "\"1\",\"64\",\"3\",\"4\",\"5\"\n"\
                    "\"1\",\"2324\",\"3\",\"4\",\"5\"\n"\
                    "\"1\",\"24\",\"3\",\"4\",\"5\"\n"\
                    "\"3\",\"2\",\"3\",\"4\",\"5\" \n"\
                    "\"13\",\"2\",\"3\",\"4\",\"5\" \n"\
                    "\"13\",\"4\",\"3\",\"4\",\"5\" \n"\
                    "\"13\",\"264\",\"3\",\"4\",\"5\""
        dict_string  = "{\"1\": {\"id\": \"1\", \"reviews\": [{\"id\": \"64\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}, {\"id\": \"2324\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}, {\"id\": \"24\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}]}, \"3\": {\"id\": \"3\", \"reviews\": [{\"id\": \"2\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}]}, \"13\": {\"id\": \"13\", \"reviews\": [{\"id\": \"2\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}, {\"id\": \"4\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}, {\"id\": \"264\", \"major_comments\": \"3\", \"minor_comments\": \"4\", \"competing_interests\": \"5\"}]}}"
        expected_dict = json.loads(dict_string)
        input_stream = StringIO(test_text)
        returned_dict = reviewercsv2bq.process_file_stream_content(input_stream)

        self.assertEqual(returned_dict, expected_dict, "Returned and Expected Dictionaries Not Equal")

    def test_parse_row(self):
        test_text_1 = " \"1\",\"2\",\"3\",\"4\",\"5 \""
        test_text_2 = " \"1 \",\"2\",\" <p> Random text </p> html tags present \",\" random text   \",\"No comment\",\"None \" "
        test_text_3 = " \"1 \",\"2\",\" <p> Random text \",\" random text   \",\"No comment\",\"None \" "

        self.assertEqual(len(reviewercsv2bq.parse_row(test_text_1)), 5,  "Size of returned list is not 5")
        self.assertEqual(len(reviewercsv2bq.parse_row(test_text_2)), 5,  "Size of returned list is not 5")
        self.assertEqual(len(reviewercsv2bq.parse_row(test_text_3)), 5,  "Size of returned list is not 5")


if __name__ == '__main__':
    unittest.main()