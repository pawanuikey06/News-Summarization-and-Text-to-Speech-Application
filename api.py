from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import process_news  # Make sure this is correct and that process_news is defined in utils.py

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for the request
class NewsRequest(BaseModel):
    company_name: str

@app.post("/analyze_news")
def analyze_news(request: NewsRequest):
    """Fetch and analyze news for a given company."""
    company_name = request.company_name

    if not company_name:
        raise HTTPException(status_code=400, detail="Company name is required")

    try:
        result = process_news(company_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing news: {str(e)}")
