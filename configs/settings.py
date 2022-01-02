import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
class Settings(BaseModel):
    authjwt_secret_key:str=os.getenv('AUTHJWT_SECRET_KEY')