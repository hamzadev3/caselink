# db.py
from sqlalchemy import create_engine, Column, Integer, String, Index, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///caselink.db", echo=False, future=True)
DBsession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class File(Base):
    __tablename__ = "files"
    id       = Column(Integer, primary_key=True)
    case_id  = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    borough  = Column(String, nullable=True)
    kind     = Column(String, nullable=True) 

    __table_args__ = (
        UniqueConstraint("filepath", name="uniq_filepath"),
        Index("idx_case_id", "case_id"),
    )

def init_db():
    Base.metadata.create_all(bind=engine)
