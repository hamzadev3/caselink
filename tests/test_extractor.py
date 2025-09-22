from extract import extract_case

def test_basic_patterns():
    assert extract_case("Bronx_(60012)_address.pdf") == "60012"
    assert extract_case("note#12345.txt") == "12345"
    assert extract_case("report_20240101_60055A.doc") == "60055"

def test_ignores_noise():
    assert extract_case("CPC_ignore_77777.pdf") is None
    assert extract_case("phone_5551234.txt") is None
