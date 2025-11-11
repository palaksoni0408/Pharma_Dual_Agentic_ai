from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Query(Base):
    """Store query history"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    model = Column(String)
    results = Column(JSON)
    tokens_used = Column(Integer)
    cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class Document(Base):
    """Store uploaded documents"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String)
    file_size = Column(Integer)
    content = Column(String)
    metadata = Column(JSON)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class UsageLog(Base):
    """Track API usage"""
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    model = Column(String)
    tokens = Column(Integer)
    cost = Column(Float)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database setup
def get_database_session(database_url: str):
    """Create database session"""
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()