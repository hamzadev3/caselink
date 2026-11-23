import pytest
from extract import extract_case


@pytest.mark.parametrize("filename, expected", [
    # valid case IDs in different layouts
    ("Bronx_60012_address.pdf", "60012"),
    ("Bronx_(60012)_address.pdf", "60012"),
    ("Queens_notes_(60034).txt", "60034"),
    ("note#12345.txt", "12345"),
    ("note # 12345.txt", "12345"),
    ("report_20240101_60055A.doc", "60055"),   # date present, ID still found
    ("Case 60012 Bronx.pdf", "60012"),         # spaces instead of underscores
    ("60012.pdf", "60012"),                    # ID at the very start
    ("60012-BK.pdf", "60012"),
    ("Data_60012.pdf", "60012"),               # "Data" is not the excluded word "DA"
])
def test_finds_case_id(filename, expected):
    assert extract_case(filename) == expected


@pytest.mark.parametrize("filename", [
    "phone_5551234.txt",        # 7-digit number, not a case ID
    "Bronx_600123_x.pdf",       # 6-digit number
    "report_20240101.doc",      # date only
    "CPC_ignore_77777.pdf",     # excluded document type
    "DA_60012.pdf",
    "plans_60012.pdf",          # exclusion is case-insensitive
    "1234.txt",                 # too short
    "no_numbers_here.txt",
])
def test_ignores_noise(filename):
    assert extract_case(filename) is None