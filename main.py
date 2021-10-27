from fastapi.routing import APIRoute
import inspect, re
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from routers.users import user_routes 
from routers.products import product_routes 
from routers.category import category_routes 
from routers.authentication import authentication 
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from models.settings import Settings


app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "Local Pasal API",
        version = "1.0",
        description = "An API for a Local Pasal Service",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route,"endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

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

