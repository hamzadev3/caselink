import re

PATTERNS = [
    re.compile(r"#\s*(\d{5})"),        # #12345
    re.compile(r"\(\s*(\d{5})\s*\)"),  # (12345)
    re.compile(r"(\d{5})(?=[A-Za-z])") # 12345A -> 12345
]

DATE_OR_SIX = re.compile(
    r"\b((?:19|20)\d{2}[01]\d[0-3]\d|"  # YYYYMMDD
    r"[0-3]\d[01]\d(?:19|20)\d{2}|"     # DDMMYYYY
    r"\d{6})\b"                          # 6-digit numbers
)

EXCLUDE_WORDS = re.compile(r"\b(PDA|DA|CPC|PLANS|RAD)\b", re.I)

def extract_case(filename: str):
    """Return the first valid 5-digit case ID, or None if no match."""
    if EXCLUDE_WORDS.search(filename) or DATE_OR_SIX.search(filename):
        return None
    for pat in PATTERNS:
        m = pat.search(filename)
        if m:
            return m.group(1)
    return None

if __name__ == "__main__":
    tests = [
        "Bronx_(60012)_address.pdf",
        "report_20240101_60055A.doc",
        "note#12345.txt",
        "phone_5551234.txt"
    ]
    for t in tests:
        print(t, "->", extract_case(t))
