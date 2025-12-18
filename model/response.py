from typing import List, Dict, Any
from pydantic import BaseModel, RootModel, Field

class OcrResponse(BaseModel):
    Product_Name: str = Field(..., alias="Product Name")
    Product_Category: str = Field(..., alias="Product Category")
    HS_Code: str = Field(..., alias="HS Code")
    Common_Trade_Name: str = Field(..., alias="Common Trade Name")

    class Config:
        allow_population_by_field_name = True

# class DataItem(BaseModel):
#     data: Dict[str, Any]

# class TrendResponseItem(BaseModel):
#     country: str
#     product_name: str
#     data: List[Dict[str, Any]]

# class TrendResponse(RootModel):
#     __root__: List[TrendResponseItem]
