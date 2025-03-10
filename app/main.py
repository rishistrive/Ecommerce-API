import time

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app import models
from app.database import engine
from app.logger import logger
from app.routes import order_routes, product_routes, user_routes


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(f"{request.method} {request.url.path} - ")

        logger.info(f"{response.status_code} (Processed in {process_time:.2f}s)")
        return response


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI application")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application")


app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)


# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint to check if the server is running.

    Returns:
        dict: A message confirming the server is running and providing
              a link to the API documentation.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Server is running. Visit /docs for API documentation."}
