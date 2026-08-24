from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class Proposal(Base):
tablename = "proposals"
id = Column(Integer, primary_key=True, index=True)
client_name = Column(String)
service_type = Column(String)
amount_cad = Column(Float)
generated_proposal = Column(Text)
Base.metadata.create_all(bind=engine)