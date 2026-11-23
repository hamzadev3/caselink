# CaseLink — Python/Regex + SQLite → API

![CI](https://github.com/hamzadev3/caselink/actions/workflows/ci.yml/badge.svg)

**What this does:**

- creates fake files with messy names in `/_sample`
- extracts the correct 5-digit case ID (avoids dates/phones/6-digit noise)
- saves results to **SQLite** (`caselink.db`)
- a tiny **API** with **/docs** (Swagger) is available to search by code

## Quick Start (Mac)

```bash
# clone & enter
# git clone https://github.com/hamzadev3/caselink.git
# cd caselink

python3 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python sample_data.py         # write fake files to _sample/
python scan.py                # build SQLite index
uvicorn api:app --reload --port 8081

# open http://localhost:8081/docs
# try GET /search?case=60012
```
## Running tests

```bash
pytest -q
```

## How case IDs are detected

- A case ID is exactly five digits with no digit directly before or after it, so dates (20240101), phone numbers and 6-digit numbers are ignored.
- `#12345` and `(12345)` are checked first; otherwise the first standalone 5-digit number wins.
- Files whose names contain PDA, DA, CPC, PLANS or RAD as a separate word are skipped.
- Known limitation: a filename with two standalone 5-digit numbers (e.g. a ZIP code and a case ID) returns the first one.
