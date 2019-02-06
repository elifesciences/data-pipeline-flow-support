import io, json, pytest
from datetime import datetime
from .. import ejpcsv2json as ecj

simplest_fixture = '''"Query: POA Received"
"Generated on November 18, 2018"
 
"poa_m_ms_id","poa_m_ms_no","poa_r_received_dt","poa_r_receipt_dt2"
"38546","27706","2017-04-11 15:38:47.637","2017-06-01 03:31:21.817"
"42025","30325","2017-07-11 08:08:57.670","2017-07-26 05:14:54.213"'''

time_frozen_at = '2018-11-01 23:59:59'

@pytest.mark.freeze_time(time_frozen_at)
def test_standard_parse():
    buffer = io.StringIO()
    writer = lambda x: buffer.write(str(x) + "\n")
    ecj.main(io.StringIO(simplest_fixture), writer)
    json_lines = buffer.getvalue().splitlines()
    actual = list(map(json.loads, json_lines))
    expected = [
        {'poa_m_ms_id': '38546', 'poa_m_ms_no': '27706', 'poa_r_received_dt': '2017-04-11 15:38:47.637', 'poa_r_receipt_dt2': '2017-06-01 03:31:21.817', 'date_generated': '2018-11-18', 'imported_timestamp': '2018-11-01T23:59:59Z'},
        {'poa_m_ms_id': '42025', 'poa_m_ms_no': '30325', 'poa_r_received_dt': '2017-07-11 08:08:57.670', 'poa_r_receipt_dt2': '2017-07-26 05:14:54.213', 'date_generated': '2018-11-18', 'imported_timestamp': '2018-11-01T23:59:59Z'}]
    assert expected == actual

@pytest.mark.freeze_time(time_frozen_at)
def test_standard_parse_with_filename():
    buffer = io.StringIO()
    writer = lambda x: buffer.write(str(x) + "\n")
    filename = "ejp_query_tool_query_id_705_DataScience:_Reviewer_identity_revealed_-_last_week_2018_10_19_eLife.csv"
    ecj.main(io.StringIO(simplest_fixture), writer, filename=filename)
    json_lines = buffer.getvalue().splitlines()
    actual = list(map(json.loads, json_lines))
    expected = [
        {'poa_m_ms_id': '38546', 'poa_m_ms_no': '27706', 'poa_r_received_dt': '2017-04-11 15:38:47.637', 'poa_r_receipt_dt2': '2017-06-01 03:31:21.817', 'date_generated': '2018-11-18', 'imported_timestamp': '2018-11-01T23:59:59Z', 'provenance': {'source_filename': filename}},
        {'poa_m_ms_id': '42025', 'poa_m_ms_no': '30325', 'poa_r_received_dt': '2017-07-11 08:08:57.670', 'poa_r_receipt_dt2': '2017-07-26 05:14:54.213', 'date_generated': '2018-11-18', 'imported_timestamp': '2018-11-01T23:59:59Z', 'provenance': {'source_filename': filename}}]
    assert expected == actual

def test_empty_fields_are_null():
    now = datetime.now()
    row = {
        "foo": "",
        "bar": " ",
        "baz": "                                          ",
        "bup": now, # non-empty, non-string field
    }
    expected_row = {
        "foo": None,
        "bar": None,
        "baz": None,
        "bup": now
    }
    assert expected_row == ecj.empty_fields_are_null(row)

def test_unescape_html_escaped_values():
    row = {
        'foo': "L&#x00E1;szl&#x00F3; Csan&#x00E1;dy",
        'bar': "László Csanády",
        'baz': "L&#x00E1;szl&#x00F3; Csanády",
    }
    expected_row = {
        'foo': "László Csanády",
        'bar': "László Csanády",
        'baz': "László Csanády",
    }
    assert expected_row == ecj.unescape_html_escaped_values(row)
