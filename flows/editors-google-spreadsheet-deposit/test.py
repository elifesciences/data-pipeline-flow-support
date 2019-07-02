import unittest
from io import StringIO
import json
from .src import editorscsv2json


class TestEditorsCsv2Json(unittest.TestCase):
    def test_process_file_stream_content(self):

        self.maxDiff = None
        test_text = (
            "Name,Keywords,Research interests,Website URL,PubMed URL\n"
            '"name1","keyword1, keyword2, keyword3","body of research, interest text","http://wwww.eexample.com:8080/sds?ruiu=researcher","http://pubmedurl.org/something?arg=value"\n'
            '"name1","keyword1, keyword2, keyword3","body of research, interest text","http://wwww.eexample.com:8080/sds?ruiu=researcher","http://pubmedurl.org/something?arg=value"\n'
            '"name2","keyword1, keyword4, keyword5","body of research interest text2","http://wwww.eexample2.com:8080/sds?ruiu=researcher","http://pubmedurl.org/something2?arg=value"\n'
        )

        expected_values = list()

        row_1 = '{"name": "name1", "keywords": "keyword1, keyword2, keyword3", "research_interests": "body of research, interest text", "website_url": "http:\/\/wwww.eexample.com:8080\/sds?ruiu=researcher", "pubmed_url": "http:\/\/pubmedurl.org\/something?arg=value", "editor_role": "BRE"}'
        row_2 = '{"name": "name1", "keywords": "keyword1, keyword2, keyword3", "research_interests": "body of research, interest text", "website_url": "http:\/\/wwww.eexample.com:8080\/sds?ruiu=researcher", "pubmed_url": "http:\/\/pubmedurl.org\/something?arg=value","editor_role": "BRE"}'
        row_3 = '{"name": "name2", "keywords": "keyword1, keyword4, keyword5", "research_interests": "body of research interest text2", "website_url": "http:\/\/wwww.eexample2.com:8080\/sds?ruiu=researcher", "pubmed_url": "http:\/\/pubmedurl.org\/something2?arg=value","editor_role": "BRE"}'
        expected_values.append(json.loads(row_1))
        expected_values.append(json.loads(row_2))
        expected_values.append(json.loads(row_3))
        input_stream = StringIO(test_text)
        output_list = list()

        def append_to_list(json_row):
            json_row = json.loads(json_row)
            json_row.pop("imported_timestamp", None)
            output_list.append(json_row)

        editorscsv2json.main(
            input=input_stream,
            output=append_to_list,
            filename="BREs",
        )

        for json_object_index in range(len(output_list)):
            self.assertEqual(
                output_list[json_object_index],
                expected_values[json_object_index],
                "Returned and Expected Dictionaries Not Equal",
            )


if __name__ == "__main__":
    unittest.main()
