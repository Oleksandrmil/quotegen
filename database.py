from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Proposal(Base):
  __tablename__ = "proposals"
  
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    service_type = Column(String)
    amount_cad = Column(Float)
    tax_cad = Column(Float)
    total_cad = Column(Float)
    proposal_text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
