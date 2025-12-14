"""
AI Analysis Service using DeepSeek and Yandex Vision
Python 3.6 compatible version
"""
import httpx
import base64
import json
from typing import Optional, Dict, Any
from ..config import settings
from ..models.schemas import DesignAnalysis, ImageAnalysis


class DeepSeekAnalyzer:
    """Analyzer using DeepSeek API for text analysis"""
    
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_url = settings.deepseek_api_url
    
    async def analyze_competitor_text(self, text: str, competitor_name: Optional[str] = None) -> DesignAnalysis:
        """Analyze competitor text using DeepSeek"""
        
        prompt = self._build_analysis_prompt(text, competitor_name)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
            {
                "role": "system",
                "content": "Ты эксперт-аналитик в области 3D-анимации и моушн-дизайна. Анализируй конкурентов и предоставляй подробные выводы. Отвечай на русском языке."
            },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
        
        # Parse response
        content = data["choices"][0]["message"]["content"]
        return self._parse_analysis_response(content)
    
    def _build_analysis_prompt(self, text: str, competitor_name: Optional[str]) -> str:
        """Build analysis prompt"""
        company_info = f"Компания: {competitor_name}\n" if competitor_name else ""
        
        return f"""{company_info}
Проанализируй этого конкурента в области 3D-анимации и моушн-дизайна:

{text}

Предоставь анализ в формате JSON на русском языке:
{{
    "design_score": <1-10>,
    "animation_potential": <1-10>,
    "innovation_score": <1-10>,
    "technical_execution": <1-10>,
    "client_focus": <1-10>,
    "strengths": ["сильная сторона 1", "сильная сторона 2", ...],
    "weaknesses": ["слабая сторона 1", "слабая сторона 2", ...],
    "style_analysis": "подробный анализ стиля",
    "improvement_recommendations": ["рекомендация 1", "рекомендация 2", ...],
    "summary": "краткое резюме"
}}"""
    
    def _parse_analysis_response(self, content: str) -> DesignAnalysis:
        """Parse AI response into DesignAnalysis model"""
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(content)
            return DesignAnalysis(**data)
        except Exception as e:
            # Fallback response
            return DesignAnalysis(
                design_score=7,
                animation_potential=7,
                innovation_score=7,
                technical_execution=7,
                client_focus=7,
                strengths=["Professional presentation"],
                weaknesses=["Analysis parsing error: " + str(e)],
                style_analysis="Unable to parse detailed analysis",
                improvement_recommendations=["Review API response format"],
                summary="Analysis completed with parsing issues"
            )


class YandexVisionAnalyzer:
    """Analyzer using Yandex Vision OCR"""
    
    def __init__(self):
        self.api_key = settings.yandex_vision_api_key
        self.folder_id = settings.yandex_vision_folder_id
        self.endpoint = settings.yandex_vision_endpoint
    
    async def analyze_image(self, image_base64: str) -> ImageAnalysis:
        """Analyze image using Yandex Vision OCR"""
        
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "folderId": self.folder_id,
            "analyze_specs": [
                {
                    "content": image_base64,
                    "features": [
                        {
                            "type": "TEXT_DETECTION",
                            "text_detection_config": {
                                "language_codes": ["en", "ru"]
                            }
                        },
                        {
                            "type": "CLASSIFICATION"
                        }
                    ]
                }
            ]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.endpoint,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
        
        # Extract text and analyze
        extracted_text = self._extract_text_from_response(data)
        
        # Use DeepSeek to analyze the visual content
        deepseek = DeepSeekAnalyzer()
        analysis_prompt = f"""Проанализируй описание дизайна/скриншота:

{extracted_text}

Предоставь визуальный анализ в формате JSON на русском языке:
{{
    "description": "краткое описание визуального контента",
    "design_score": <1-10>,
    "animation_potential": <1-10>,
    "visual_style_score": <1-10>,
    "visual_style_analysis": "подробный анализ стиля",
    "recommendations": ["рекомендация 1", "рекомендация 2", ...]
}}"""
        
        headers_deepseek = {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        payload_deepseek = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Ты эксперт по визуальному дизайну. Отвечай на русском языке."},
                {"role": "user", "content": analysis_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.deepseek_api_url,
                headers=headers_deepseek,
                json=payload_deepseek
            )
            response.raise_for_status()
            data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        return self._parse_image_analysis(content, extracted_text)
    
    def _extract_text_from_response(self, response_data: Dict[str, Any]) -> str:
        """Extract text from Yandex Vision response"""
        try:
            texts = []
            for result in response_data.get("results", []):
                for detection in result.get("results", []):
                    if detection.get("textDetection"):
                        for page in detection["textDetection"].get("pages", []):
                            for block in page.get("blocks", []):
                                for line in block.get("lines", []):
                                    for word in line.get("words", []):
                                        texts.append(word.get("text", ""))
            return " ".join(texts) or "No text detected in image"
        except Exception:
            return "Error extracting text from image"
    
    def _parse_image_analysis(self, content: str, extracted_text: str) -> ImageAnalysis:
        """Parse image analysis response"""
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(content)
            return ImageAnalysis(**data)
        except Exception as e:
            return ImageAnalysis(
                description=extracted_text[:200] if extracted_text else "Image analysis",
                design_score=7,
                animation_potential=7,
                visual_style_score=7,
                visual_style_analysis="Visual analysis completed",
                recommendations=["Unable to parse detailed recommendations: " + str(e)]
            )


# Global instances
deepseek_analyzer = DeepSeekAnalyzer()
yandex_vision_analyzer = YandexVisionAnalyzer()
