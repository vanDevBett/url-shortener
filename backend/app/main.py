from fastapi import FastAPI

from app.api.links import router as links_router

app = FastAPI(title="URL Shortener")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"mensaje": "¡Welcome to my API URL Shortener!"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(links_router)
