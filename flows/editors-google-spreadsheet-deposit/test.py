"""
unittest editorscsv2json.py
"""
import unittest
from io import StringIO
import json
from src import editorscsv2json


class TestEditorsCsv2Json(unittest.TestCase):
    def test_process_file_stream_content(self):
        self.maxDiff = None
        test_text = (
            "Name,Subject areas,Keywords,Research interests,Website URL,"
            "PubMed URL,Relevant PubMed URLs\n"
            '"name1","subject1, subject4, subject5","keyword1, keyword2, keyword3",'
            '"body of research, interest text",'
            '"http://wwww.eexample.com:8080/sds?ruiu=researcher",'
            '"http://pubmedurl.org/something?arg=value","url1, url2"\n'
            '"name1","subject1","keyword1, keyword2, keyword3",'
            '"body of research, interest text",'
            '"http://wwww.eexample.com:8080/sds?ruiu=researcher",'
            '"http://pubmedurl.org/something?arg=value","url3, url4"\n'
            '"name2","subject7","keyword1, keyword4, keyword5",'
            '"body of research interest text2",'
            '"http://wwww.eexample2.com:8080/sds?ruiu=researcher",'
            '"http://pubmedurl.org/something2?arg=value","url5, url6"\n'
        )
        current_time = "2019-10-16 08:24:32 +0100"
        expected_values = list()

        row_1 = r'{"name": "name1","subject_areas":"subject1, subject4, subject5",' \
                r' "keywords": "keyword1, keyword2, keyword3", "research_interests": ' \
                r'"body of research, interest text",' \
                r' "website_url": "http://wwww.eexample.com:8080/sds?ruiu=researcher", ' \
                r'"pubmed_url": "http://pubmedurl.org/something?arg=value",' \
                r'"relevant_pubmed_urls":"url1, url2",' \
                r' "editor_role": "BRE", "imported_timestamp":"2019-10-16T07:24:32Z"}'
        row_2 = r'{"name": "name1", "subject_areas":"subject1", ' \
                r'"keywords": "keyword1, keyword2, keyword3", ' \
                r'"research_interests": "body of research, interest text",' \
                r' "website_url": "http://wwww.eexample.com:8080/sds?ruiu=researcher", ' \
                r'"pubmed_url": "http://pubmedurl.org/something?arg=value",' \
                r'"relevant_pubmed_urls":"url3, url4",' \
                r'"editor_role": "BRE", "imported_timestamp":"2019-10-16T07:24:32Z"}'
        row_3 = r'{"name": "name2","subject_areas":"subject7", ' \
                r'"keywords": "keyword1, keyword4, keyword5", ' \
                r'"research_interests": "body of research interest text2", ' \
                r'"website_url": "http://wwww.eexample2.com:8080/sds?ruiu=researcher", ' \
                r'"pubmed_url": "http://pubmedurl.org/something2?arg=value",' \
                r'"relevant_pubmed_urls":"url5, url6",' \
                r'"editor_role": "BRE", "imported_timestamp":"2019-10-16T07:24:32Z"}'
        expected_values.append(json.loads(row_1))
        expected_values.append(json.loads(row_2))
        expected_values.append(json.loads(row_3))
        input_stream = StringIO(test_text)
        output_list = list()

        def append_to_list(json_row):
            json_row = json.loads(json_row)
            output_list.append(json_row)

        editorscsv2json.main(
            input=input_stream,
            output=append_to_list,
            filename="filename_BRE",
            time_now=current_time,
        )

        for json_object_index, _ in enumerate(output_list):
            self.assertEqual(
                output_list[json_object_index],
                expected_values[json_object_index],
                "Returned and Expected Dictionaries Not Equal",
            )


if __name__ == "__main__":
    unittest.main()
