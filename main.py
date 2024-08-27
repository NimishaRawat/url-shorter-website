from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import string
import random
from starlette.responses import RedirectResponse

app = FastAPI()

# Serve the static directory for CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Database setup (replace with your NeonDB connection string)
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:PYakpyNIFe54@ep-snowy-wind-a58ryim4.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

class URLInput(BaseModel):
    url: HttpUrl

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/shorten")
async def shorten_url(request: Request, url: str = Form(...)):
    db = SessionLocal()
    
    # Check if URL already exists
    existing_url = db.query(URL).filter(URL.original_url == url).first()
    if existing_url:
        short_url = f"http://localhost:8000/{existing_url.short_code}"
        return templates.TemplateResponse("result.html", {"request": request, "short_url": short_url})
    
    # Generate a unique short code
    while True:
        short_code = generate_short_code()
        if not db.query(URL).filter(URL.short_code == short_code).first():
            break
    
    # Create new URL entry
    new_url = URL(original_url=url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    
    short_url = f"http://localhost:8000/{short_code}"
    return templates.TemplateResponse("result.html", {"request": request, "short_url": short_url})


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    db = SessionLocal()
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        return RedirectResponse(url.original_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
