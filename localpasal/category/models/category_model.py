from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    categoryName: str
    categoryImage: str
    subCategories: list

