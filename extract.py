import re

# A case ID is a run of EXACTLY five digits: no digit directly before it,
# no digit directly after it. This rejects pieces of longer numbers
# (dates like 20240101, phone numbers like 5551234, 6-digit IDs).
FIVE_DIGITS = r"(?<!\d)(\d{5})(?!\d)"

# Checked in order: explicit markers first, then any standalone 5-digit run.
PATTERNS = [
    re.compile(r"#\s*" + FIVE_DIGITS),              # note#12345
    re.compile(r"\(\s*" + FIVE_DIGITS + r"\s*\)"),  # notes_(60034)
    re.compile(FIVE_DIGITS),                        # Bronx_60012_address
]

# Document types we never index. The word must not touch another letter,
# so "CPC_ignore" and "DA_60012" match, but "Data" or "Radio" do not.
EXCLUDE_WORDS = re.compile(r"(?<![A-Za-z])(PDA|DA|CPC|PLANS|RAD)(?![A-Za-z])", re.I)


def extract_case(filename: str):
    """Return the 5-digit case ID in a filename, or None if there isn't one."""
    if EXCLUDE_WORDS.search(filename):
        return None
    for pat in PATTERNS:
        m = pat.search(filename)
        if m:
            return m.group(1)
    return None


if __name__ == "__main__":
    tests = [
        "Bronx_60012_address.pdf",
        "report_20240101_60055A.doc",
        "note#12345.txt",
        "phone_5551234.txt",
        "CPC_ignore_77777.pdf",
    ]
    print("--- DEBUG TEST ---")
    for t in tests:
        print(f"File: {t} -> Extracted: {extract_case(t)}")