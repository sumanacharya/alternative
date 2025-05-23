from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, ValidationError
from search import google_dork_search
import asyncio
from typing import Dict, List

app = FastAPI(
    title="Email Shield POC",
    description="A service that analyzes email addresses for potential security risks using Google dorking",
    version="1.0.0"
)

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    source: str

class EmailRequest(BaseModel):
    email: EmailStr

class EmailFeatures(BaseModel):
    total_mentions: int
    pastebin_mentions: int
    github_mentions: int
    stackoverflow_mentions: int
    total_results: List[SearchResult]
    pastebin_results: List[SearchResult]
    github_results: List[SearchResult]
    stackoverflow_results: List[SearchResult]

async def safe_dork_search(query: str) -> tuple[int, List[Dict]]:
    """Safely perform a dork search with timeout"""
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(google_dork_search, query),
            timeout=10.0  # 10 second timeout
        )
    except asyncio.TimeoutError:
        print(f"Timeout while searching for: {query}")
        return 0, []
    except Exception as e:
        print(f"Error searching for {query}: {str(e)}")
        return 0, []

@app.post("/v1/analyze/email", response_model=EmailFeatures)
async def analyze_email(req: EmailRequest):
    """
    Analyze an email address for potential security risks using Google dorking.
    
    Args:
        req (EmailRequest): The email address to analyze
        
    Returns:
        EmailFeatures: Analysis results including mention counts and detailed results from various sources
    """
    try:
        e = req.email
        # Build dork queries
        q_general = f"intext:{e}"
        q_paste = f"site:pastebin.com intext:{e}"
        q_github = f"site:github.com intext:{e}"
        q_stack = f"site:stackoverflow.com intext:{e}"
        
        # Fetch results concurrently
        tasks = [
            safe_dork_search(q_general),
            safe_dork_search(q_paste),
            safe_dork_search(q_github),
            safe_dork_search(q_stack)
        ]
        results = await asyncio.gather(*tasks)
        
        # Unpack results
        total_count, total_results = results[0]
        paste_count, paste_results = results[1]
        github_count, github_results = results[2]
        stack_count, stack_results = results[3]
        
        return {
            "total_mentions": total_count,
            "pastebin_mentions": paste_count,
            "github_mentions": github_count,
            "stackoverflow_mentions": stack_count,
            "total_results": total_results,
            "pastebin_results": paste_results,
            "github_results": github_results,
            "stackoverflow_results": stack_results
        }
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 