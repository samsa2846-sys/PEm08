"""
FastAPI Main Application - Python 3.6 compatible
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
from pathlib import Path

from .config import settings
from .models.schemas import (
    TextAnalysisRequest,
    ParseRequest,
    AnalysisResponse,
    ImageAnalysisResponse
)
from .services.analyzer_service import deepseek_analyzer, yandex_vision_analyzer

# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    root_path="/pem08"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def root():
    """Serve frontend"""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "MotionCraft AI Analyzer API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "services": {
            "deepseek": bool(settings.deepseek_api_key),
            "yandex_vision": bool(settings.yandex_vision_api_key),
            "parser": False
        }
    }


@app.post("/analyze_text", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyze competitor text"""
    try:
        if not settings.deepseek_api_key:
            raise HTTPException(status_code=503, detail="DeepSeek API key not configured")
        
        analysis = await deepseek_analyzer.analyze_competitor_text(
            text=request.text,
            competitor_name=request.competitor_name
        )
        
        return AnalysisResponse(success=True, analysis=analysis)
    
    except Exception as e:
        return AnalysisResponse(success=False, detail=str(e))


@app.post("/analyze_image", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze image"""
    try:
        if not settings.yandex_vision_api_key:
            raise HTTPException(status_code=503, detail="Yandex Vision API key not configured")
        
        # Read and encode image
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode('utf-8')
        
        analysis = await yandex_vision_analyzer.analyze_image(image_base64)
        
        return ImageAnalysisResponse(success=True, analysis=analysis)
    
    except Exception as e:
        return ImageAnalysisResponse(success=False, detail=str(e))


@app.post("/parse_demo")
async def parse_demo(request: ParseRequest):
    """Demo parsing endpoint (simplified)"""
    return JSONResponse(
        content={
            "success": True,
            "url": request.url,
            "text_preview": "Demo: Parsing functionality requires Selenium setup",
            "analysis": None
        }
    )


@app.get("/history")
async def get_history():
    """Get analysis history"""
    return {"items": [], "total": 0}


@app.delete("/history")
async def clear_history():
    """Clear history"""
    return {"success": True, "message": "History cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
