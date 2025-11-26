import re

PATTERNS = [
    re.compile(r"#\s*(\d{5})"),          
    re.compile(r"\(\s*(\d{5})\s*\)"),    
    re.compile(r"(\d{5})(?=[A-Za-z])"),  
    re.compile(r"(\d{5})_"),             
    re.compile(r"_(\d{5})")              
]

DATE_OR_SIX = re.compile(
    r"\b((?:19|20)\d{2}[01]\d[0-3]\d|[0-3]\d[01]\d(?:19|20)\d{2}|\d{6})\b"
)

EXCLUDE_WORDS = re.compile(r"\b(PDA|DA|CPC|PLANS|RAD)\b", re.I)

def extract_case(filename: str):
    if EXCLUDE_WORDS.search(filename) or DATE_OR_SIX.search(filename):
        return None
    for pat in PATTERNS:
        m = pat.search(filename)
        if m:
            return m.group(1)
    return None

if __name__ == "__main__":
    # Test script to verify it works instantly
    tests = [
        "Bronx_60012_address.pdf",
        "report_20240101_60055A.doc",
        "note#12345.txt",
        "phone_5551234.txt",
        "CPC_ignore_77777.pdf"
    ]
    print("--- DEBUG TEST ---")
    for t in tests:
        res = extract_case(t)
        print(f"File: {t} -> Extracted: {res}")