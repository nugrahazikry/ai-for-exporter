from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from generation_pipeline.ocr_main_function import ai_ocr_processing, ocr_correction_function
from generation_pipeline.export_trend_main_function import extract_trend_data
import asyncio
from typing import List, Dict, Any
from model.request import (
    OcrCorrection,
    TrendRequest
)

from model.response import (
    OcrResponse
)

app = FastAPI()
    

@app.post("/ocr/*", response_model=OcrResponse)
async def ocr_endpoint(image: UploadFile = File(...), language: str = Form(...)):
    try:
        result = await asyncio.to_thread(ai_ocr_processing, image, language)
        return OcrResponse(**result)
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ocr-correction/*", response_model=OcrResponse)
async def ocr_correction_endpoint(request: OcrCorrection):
    try:
        result = await asyncio.to_thread(ocr_correction_function, request.correct_product, request.language)
        return OcrResponse(**result)
        
    except Exception as e:
        return JSONResponse(status_code=500,content={"error": str(e)})


@app.post("/trend-analysis/*")
async def trend_analysis_endpoint(request: TrendRequest):
    try:
        result = await asyncio.to_thread(extract_trend_data, request.hs_code, request.product_name)
        return JSONResponse(content=result)
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})