# CaseLink — Python/Regex + SQLite → API

**\What this does:**

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
