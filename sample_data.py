# sample_data.py
from pathlib import Path

SAMPLES = [
    "Bronx_60012_address.pdf",
    "Queens_notes_(60034).txt",
    "report_20240101_60055A.doc",
    "note#12345.txt",
    "phone_5551234.txt",
    "CPC_ignore_77777.pdf",  # will be excluded later
]

def make_samples(root="_sample"):
    rootp = Path(root)
    rootp.mkdir(parents=True, exist_ok=True)
    for name in SAMPLES:
        p = rootp / name
        p.write_text("fake content\n")
    print(f"Created {len(SAMPLES)} sample files in {rootp.resolve()}")

if __name__ == "__main__":
    make_samples()
