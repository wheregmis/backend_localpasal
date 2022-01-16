from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    productTitle: str
    productPrice: str
    productCategory: str
    productSubCategory: str
    productDescription: str
    productImage: Optional [str]
    sellerUid: str
    timestamp: str

