import time
import uuid
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

# Your assigned CORS origin
ALLOWED_ORIGIN = "https://dash-fpcjg3.example.com"

# Add CORS middleware - ONLY the allowed origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],  # No wildcard!
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware to add required headers
@app.middleware("http")
async def add_required_headers(request, call_next):
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    # Add X-Request-ID (unique per request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    
    # Add X-Process-Time (handler duration in seconds)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    # Parse comma-separated integers
    try:
        numbers = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "All values must be integers"}
        )
    
    if not numbers:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one value is required"}
        )
    
    # Compute descriptive statistics
    count = len(numbers)
    total = sum(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    mean = total / count
    
    return {
        "email": "24f2002887@ds.study.iitm.ac.in",  # REPLACE THIS with your actual email
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": mean
    }
