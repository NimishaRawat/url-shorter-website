from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import string
import random

# Database configuration
DATABASE_URL = "postgresql://rktaakash:veZ4y8YDHMmz@ep-withered-shadow-a5yk6cvp.us-east-2.aws.neon.tech/cohort?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# URL model
class URL(Base):
    tablename = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)

# Pydantic model for URL input
class URLInput(BaseModel):
    url: str

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generate a random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.post("/shorten")
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    db_url = URL(original_url=url_input.url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}

# GET /{short_code} endpoint
@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"url": db_url.original_url}

# Create the database tables
Base.metadata.create_all(bind=engine)