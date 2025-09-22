# scan.py
import os
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from db import init_db, DBsession, File
from extract import extract_case

def infer_borough(filename: str) -> str | None:
    name = filename.lower()
    for b in ["bronx", "brooklyn", "queens", "manhattan", "statenisland", "staten_island"]:
        if b in name:
            return b.title().replace("_", " ")
    return None

def infer_kind(filename: str) -> str | None:
    suffix = Path(filename).suffix.lower().lstrip(".")
    return suffix or None

def scan_folder(root="_sample") -> int:
    init_db()
    s = DBsession()
    added = 0
    try:
        for dirpath, _, files in os.walk(root):
            for fn in files:
                case_id = extract_case(fn)
                if not case_id:
                    continue
                path = str(Path(dirpath) / fn)
                row = File(
                    case_id=case_id,
                    filepath=path,
                    borough=infer_borough(fn),
                    kind=infer_kind(fn),
                )
                try:
                    s.add(row)
                    s.commit()
                    added += 1
                except IntegrityError:
                    s.rollback()  # duplicate filepath, ignore
    finally:
        s.close()
    return added

if __name__ == "__main__":
    count = scan_folder("_sample")
    print(f"Added {count} row(s) to caselink.db")
