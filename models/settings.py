from pydantic import BaseModel
import os
from dotenv import load_dotenv

class Settings(BaseModel):
    authjwt_secret_key:str=os.getenv('AUTHJWT_SECRET_KEY')