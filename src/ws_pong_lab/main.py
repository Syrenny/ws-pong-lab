from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ws_pong_lab.settings import app_config


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""],
)
prefix = "/api"
app.include_router(completions_router, prefix=prefix)


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        host=app_config.uvicorn.host,
        port=app_config.uvicorn.port,
        workers=app_config.uvicorn.workers,
        reload=app_config.uvicorn.reload,
    )
