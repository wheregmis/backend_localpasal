from pydantic import BaseModel

class Product(BaseModel):
    product_name: str
    product_description: str
    product_price: str