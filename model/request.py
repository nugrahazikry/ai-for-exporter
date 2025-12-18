from pydantic import BaseModel

class OcrCorrection(BaseModel):
    correct_product: str
    language: str

class TrendRequest(BaseModel):
    hs_code: str
    product_name: str