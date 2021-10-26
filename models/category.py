from pydantic import BaseModel

class Category(BaseModel):
    category_name: str
    category_image: str
    sub_categories: list
    brands_models: list