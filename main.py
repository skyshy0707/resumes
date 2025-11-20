from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.router import service

origins = [
    "http://localhost:9000",
    "http://localhost:9006"
]

app = FastAPI(
    docs_url="/docs",
    openapi_prefix="/api",
    title="Resumes",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(service.router)