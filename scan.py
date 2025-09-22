import os
from pathlib import Path
from extract import extract_case

def scan_folder(root="_sample"):
    results = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            case_id = extract_case(fn)
            if case_id:
                results.append((case_id, str(Path(dirpath) / fn)))
    return results

if __name__ == "__main__":
    found = scan_folder("_sample")
    for cid, path in found:
        print(f"Found case {cid} in {path}")
