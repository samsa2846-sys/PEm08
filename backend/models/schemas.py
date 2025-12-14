"""
Pydantic models for request/response validation
"""
from typing import Optional, List
from pydantic import BaseModel


class TextAnalysisRequest(BaseModel):
    text: str
    competitor_name: Optional[str] = None


class ImageAnalysisRequest(BaseModel):
    image_base64: str


class ParseRequest(BaseModel):
    url: str


class DesignAnalysis(BaseModel):
    design_score: int
    animation_potential: int
    innovation_score: int
    technical_execution: int
    client_focus: int
    strengths: List[str]
    weaknesses: List[str]
    style_analysis: str
    improvement_recommendations: List[str]
    summary: str


class ImageAnalysis(BaseModel):
    description: str
    design_score: int
    animation_potential: int
    visual_style_score: int
    visual_style_analysis: str
    recommendations: List[str]


class AnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[DesignAnalysis] = None
    detail: Optional[str] = None


class ImageAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[ImageAnalysis] = None
    detail: Optional[str] = None
