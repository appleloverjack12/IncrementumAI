from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255))
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    market = Column(String(100))
    industry = Column(String(100))
    
    # BANT Scores
    budget_score = Column(Integer)  # 0-100
    authority_score = Column(Integer)  # 0-100
    need_score = Column(Integer)  # 0-100
    timeline_score = Column(Integer)  # 0-100
    overall_score = Column(Integer)  # 0-100
    
    # Additional info
    lead_info = Column(Text)
    qualification_report = Column(Text)
    recommended_actions = Column(Text)
    conversion_probability = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(50), default='new')  # new, contacted, qualified, converted, lost

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./leads.db')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()