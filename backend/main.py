from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io

from routes.clean import clean_data
from routes.generate import generate_data
from routes.embed import vectorize_data
from routes.enrich import enrich_data
from routes.download import router as download_router

app = FastAPI(title="DataSanity API", description="AI-powered data processing API")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include download router
app.include_router(download_router)

@app.get("/")
async def root():
    return {"message": "DataSanity API is running"}

@app.post("/api/process")
async def process_data(prompt: str = Form(...), file: UploadFile = File(None)):
    # Read file if provided
    df = None
    if file and file.filename:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    # Parse prompt to determine which actions to take
    # This is a simplified parser - in a real application, you might use an LLM to parse this
    actions = []
    if "clean" in prompt.lower():
        actions.append("clean")
    if "generate" in prompt.lower():
        actions.append("generate")
    if "vectorize" in prompt.lower() or "embed" in prompt.lower():
        actions.append("embed")
    if "enrich" in prompt.lower():
        actions.append("enrich")
    
    # Process data based on requested actions
    results = {}
    
    if "clean" in actions:
        results["cleanedData"] = clean_data(df, prompt) if df is not None else "No data provided for cleaning"
    
    if "generate" in actions:
        results["generatedData"] = generate_data(prompt)
    
    if "embed" in actions:
        results["vectorizedData"] = vectorize_data(df, prompt) if df is not None else "No data provided for vectorization"
    
    if "enrich" in actions:
        results["enrichedData"] = enrich_data(df, prompt) if df is not None else "No data provided for enrichment"
    
    return JSONResponse(content=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
