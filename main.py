
from fastapi import FastAPI
from routers.users import user_routes 
from routers.products import product_routes 
from routers.category import category_routes 
from routers.authentication import authentication 
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from models.settings import Settings


app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# users.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(category_routes.category)
app.include_router(product_routes.product)
app.include_router(user_routes.user)

