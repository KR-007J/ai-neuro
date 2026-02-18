"""
Main FastAPI Application Entry Point
AI-Enabled Neuro-Cognitive Adaptive Learning Framework
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.config import settings
from app.api import routes_adaptation, routes_assessment, routes_user
from app.utils.logger import setup_logger
import time

# Initialize logger
logger = setup_logger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="Neuro-Cognitive Adaptive Learning API",
    description="AI-powered adaptive learning framework with cognitive profiling and personalized content delivery",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
    return response

# Include routers
app.include_router(
    routes_user.router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    routes_assessment.router,
    prefix="/api/v1/assessment",
    tags=["Assessment"]
)

app.include_router(
    routes_adaptation.router,
    prefix="/api/v1/adaptation",
    tags=["Adaptation"]
)

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "online",
        "message": "Neuro-Cognitive Adaptive Learning API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "models_loaded": True  # Add actual model loading check
    }

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Neuro-Cognitive Adaptive Learning API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    # Load ML models here if needed
    logger.info("API startup complete!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API...")
    # Cleanup resources here
    logger.info("Shutdown complete!")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
