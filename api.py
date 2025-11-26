from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db import init_db, DBsession, File
import tempfile
from openpyxl import Workbook

app = FastAPI(title="CaseLink API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

# --- dependency injection ---
def get_db():
    db = DBsession()
    try:
        yield db
    finally:
        db.close()

@app.get("/search")
def search(case: str = Query(..., min_length=4, max_length=5), s: Session = Depends(get_db)):
    print(f"[search] case={case}")
    rows = s.query(File).filter(File.case_id == case).limit(500).all()
    return {
        "count": len(rows),
        "results": [
            {"case": r.case_id, "filepath": r.filepath, "borough": r.borough, "kind": r.kind}
            for r in rows
        ]
    }

@app.get("/cases")
def cases(limit: int = 50, offset: int = 0, s: Session = Depends(get_db)):
    q = s.query(File.case_id).distinct().offset(offset).limit(limit)
    return {"cases": [c[0] for c in q.all()]}

@app.get("/export")
def export(case: str, s: Session = Depends(get_db)):
    rows = s.query(File).filter(File.case_id == case).limit(1000).all()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"
    ws.append(["case_id", "filepath", "borough", "kind"])

    for r in rows:
        ws.append([r.case_id, r.filepath, r.borough or "", r.kind or ""])

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    wb.save(tmp.name)
    wb.close()
    return FileResponse(tmp.name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"caselink_{case}.xlsx")